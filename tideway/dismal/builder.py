# Discovery API report builder for DisMAL

import logging
import os
from functools import lru_cache
import ipaddress

import tideway
from collections import defaultdict

from . import api, tools, output, queries, cache

logger = logging.getLogger("_builder_")


@lru_cache(maxsize=None)
def _range_to_networks(range_str):
    """Return a list of :mod:`ipaddress` networks for *range_str*.

    The results are cached so repeated ranges are only parsed once.
    """
    networks = []
    if not range_str:
        return networks
    for part in range_str.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            networks.append(ipaddress.ip_network(part, strict=False))
        except ValueError:
            logger.warning("Unable to parse scan range %s", part)
    return networks

def get_credentials(entry):
    details = {}
    uuid = entry.get('uuid')
    index = entry.get('index')
    label = entry.get('label')
    enabled = entry.get('enabled')
    types = entry.get('types')
    usage = entry.get('usage')
    username = None
    if 'username' in entry:
        username = entry.get('username')
    elif 'snmp.v3.securityname' in entry:
        username = entry.get('snmp.v3.securityname')
    elif 'aws.access_key_id' in entry:
        username = entry.get('aws.access_key_id')
    elif 'azure.application_id' in entry:
        username = entry.get('azure.application_id')
    iprange = None
    exclusions = None
    if 'ip_range' in entry:
        iprange = entry.get('ip_range')
    if 'ip_exclusion' in entry:
        exclusions = entry.get('ip_exclusion')
    details = {"index":index,"uuid":uuid,"label":label,"username":username,"enabled":enabled,"iprange":iprange,"exclusions":exclusions,"types":types,"usage":usage}
    return details

def get_credential(twsearch, twcreds, args):
    uuid = args.excavate[1]
    msg = "\nCredential Lookup: %s" % uuid
    logger.info(msg)
    print(msg)
    print("---------------------------------------------------")

    vaultcreds = twcreds.get_vault_credential(uuid)
    print(vaultcreds.text)
    vaultcredJSON = api.get_json(vaultcreds)
    if 'code' in vaultcredJSON and vaultcredJSON['code'] == 404:
        label = vaultcredJSON['message']
        i = None
        found = False
        logger.debug("Vault lookup failed: %s"%(label))
    else:
        label = vaultcredJSON['label']
        i = vaultcredJSON['index']
        found = True
        logger.debug("Vault lookup succeeded: %s"%(label))

    qryJSON = {
                "query":
                """search SessionResult
                    where credential = '%s' show
                    (#Detail:Metadata:DiscoveryAccess:DiscoveryAccess.#Associate:Inference:InferredElement:.name or #Detail:Metadata:DiscoveryAccess:DiscoveryAccess.#DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.hostname) as 'device_name',
                    (kind(#Detail:Metadata:DiscoveryAccess:DiscoveryAccess.#Associate:Inference:InferredElement:) or #Detail:Metadata:DiscoveryAccess:DiscoveryAccess.inferred_kind or #Detail:Metadata:DiscoveryAccess:DiscoveryAccess.#DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.kind) as 'inferred_node',
                    #Detail:Metadata:DiscoveryAccess:DiscoveryAccess.endpoint as 'scanned_endpoint',
                    credential as 'credential',
                    success as 'success',
                    message as 'message',
                    friendlyTime(time_index) as 'date_time',
                    #Detail:Metadata:DiscoveryAccess:DiscoveryAccess.#id as 'node_id'""" % uuid
               }
    sessionResults = api.search_results(twsearch,qryJSON)

    diJSON = {
                "query":
                """search DeviceInfo where last_credential = '%s' or last_slave = '%s' or __preserved_last_credential = '%s'
                            ORDER BY hostname
                            show
                            (hostname or sysname) as 'device_name',
                            kind as 'inferred_node',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.endpoint as 'scanned_endpoint',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.#id as 'da_node_id',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.reason as 'message',
                            method_success as 'success',
                            method_failure as 'failure',
                            friendlyTime(request_time) as 'date_time'""" % (uuid, uuid, uuid)
               }
    diResults = api.search_results(twsearch,diJSON)

    # Build the results
    
    data = []
    da_ids = []
    for result in sessionResults:
        logger.debug("Adding session result: %s"%(result))
        dn = tools.getr(result,'device_name',None)
        ifn = tools.getr(result,'inferred_node',None)
        se = tools.getr(result,'scanned_endpoint',None)
        m = tools.getr(result,'message',None)
        s = tools.getr(result,'success',None)
        dt = tools.getr(result,'date_time',None)
        id = tools.getr(result,'node_id',None)
        if id:
            da_ids.append(id)
            logger.debug("Adding DA ID to list: %s"%(id))
        data.append([ label, i, uuid, dn, ifn, se, m, s, dt ])

    for result in diResults:
        logger.debug("Checking DevicInfo result: %s"%(result))
        dn = tools.getr(result,'device_name',None)
        ifn = tools.getr(result,'inferred_node',None)
        se = tools.getr(result,'scanned_endpoint',None)
        m = tools.getr(result,'message',None)
        sx = tools.getr(result,'success',None)
        f = tools.getr(result,'failure',None)
        if sx:
            s = True
        elif f:
            s = False
        dt = tools.getr(result,'date_time',None)
        da_id = tools.getr(result,'da_node_id',None)
        if da_id and da_id in da_ids:
            logger.debug("DeviceInfo already logged in Session Result list: %s"%(da_id))
            continue # Do not log this result
        else:
            logger.debug("Adding DeviceInfo result: %s"%(da_id))
            data.append([ label, i, uuid, dn, ifn, se, m, s, dt ])

    output.report(data, [
                            "Credential",
                            "Index",
                            "UUID",
                            "Device Name",
                            "Inferred Node",
                            "Scanned Endpoint",
                            "Result/Reason",
                            "Successful",
                            "Access Time"
                        ], args, name="devices_with_cred")

    return found

def ordering(creds, search, args, apply):

    credlist = api.get_json(creds.get_vault_credentials)
    msg = "Analysing current credential order...\n"
    print(msg)
    logger.info(msg)

    if not credlist:
        msg = "Credential list could not be retrieved."
        print(msg)
        logger.error(msg)
        return

    outpost_map = {}
    if getattr(args, "target", None) and hasattr(tideway, "appliance"):
        try:
            token = getattr(args, "token", None)
            if not token and getattr(args, "f_token", None):
                if os.path.isfile(args.f_token):
                    with open(args.f_token, "r") as f:
                        token = f.read().strip()
            app = tideway.appliance(args.target, token)
            outpost_map = api.map_outpost_credentials(app)
            logger.debug("Outpost credential map: %s", outpost_map)
        except Exception as e:  # pragma: no cover - network errors
            logger.error("Failed to retrieve outpost credentials: %s", e)

    cred_weighting = []
    
    for cred in credlist:
        weighting = 100
        label = cred.get('label')
        index = cred.get('index')
        #if not args.weigh:
        #    msg = '%s) %s' % (index, label)
        #    print(msg)
        #    logger.info(msg)
        
        # Weightings

        if "ip_range" in cred:
            ip_list = tools.range_to_ips(cred.get('ip_range'))
            for ip in ip_list:
                if ip == "0.0.0.0/0,::/0":
                    weighting = 4294967296 # Go to the bottom, (total no. IPs in the world)
                else:
                    weighting += 1
            logger.debug("Credential %s, IP Range: %s, Weighting Updated: %s"%(label,ip_list,weighting))

        if "ip_exclusion" in cred:
            exclude_list = tools.range_to_ips(cred.get('ip_exclusion'))
            for ip in exclude_list:
                if ip == "0.0.0.0/0,::/0":
                    weighting = -4294967296 # Will scan nothing - who would set this? No doubt there will be a customer out there!
                else:
                    weighting -= 1
            logger.debug("Credential %s, Exclude List: %s, Weighting Updated: %s"%(label,exclude_list,weighting))

        for type in cred['types']:
            if type == "aws" or type == "openstack" or type == "azure" or type == "web_basic" or type == "google":
                weighting += 1
                logger.debug("Credential %s, Type: %s, Weighting Updated: %s"%(label,type,weighting))
            elif type == "ssh" or type == "powershell":
                weighting += 2
                logger.debug("Credential %s, Type: %s, Weighting Updated: %s"%(label,type,weighting))
            elif type == "windows":
                weighting += 3
                logger.debug("Credential %s, Type: %s, Weighting Updated: %s"%(label,type,weighting))
            elif type == "vsphere" or type == "vcenter":
                weighting += 4
                logger.debug("Credential %s, Type: %s, Weighting Updated: %s"%(label,type,weighting))
            elif type == "snmp":
                weighting += 5
                logger.debug("Credential %s, Type: %s, Weighting Updated: %s"%(label,type,weighting))
            else:
                weighting += 6
                logger.debug("Credential %s, No Type, Weighting Updated: %s"%(label,weighting))

        if "ssh.key.set" in cred:
            ssh_key_set = cred.get('ssh.key.set')
            if ssh_key_set:
                weighting -= 1
                logger.debug("Credential %s, SSH Key Set, Weighting Updated: %s"%(label,weighting))

        if "snmp.version" in cred:
            snmp_version = cred.get('snmp.version')
            if snmp_version == "v3":
                weighting -= 1
                logger.debug("Credential %s, SNMPv3, Weighting Updated: %s"%(label,weighting))

        if "scopes" in cred:
            scopes = cred.get('scopes')
            if len(scopes) > 0:
                weighting -= 1
                logger.debug("Credential %s, in Scope, Weighting Updated: %s"%(label,weighting))

        ## Successes and Failures

        seshsux = api.search_results(search,"""
                                        search SessionResult where success
                                        and (slave = "%s" or credential = "%s")
                                        show (credential or slave) as cred_uuid, session_type process with countUnique(0)
                                        """ % (cred['uuid'],cred['uuid']))
        devinfosux = api.search_results(search,"""
                                        search DeviceInfo where method_success
                                        and (slave = "%s" or credential = "%s")
                                        and nodecount(traverse DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess traverse DiscoveryAccess:Metadata:Detail:SessionResult) = 0
                                        show (last_credential or last_slave) as cred_uuid,
                                        access_method as 'session_type'
                                        process with countUnique(0)
                                    """ % (cred['uuid'],cred['uuid']))
        credfails = api.search_results(search,"""
                                        search SessionResult where not success
                                        and (slave = "%s" or credential = "%s")
                                        show (credential or slave) as cred_uuid, session_type process with countUnique(0)
                                    """ % (cred['uuid'],cred['uuid']))
        
        for credsux in seshsux:
            weighting -= 1
            logger.debug("Credential %s, Counted Successful Session record, Weighting Updated: %s"%(label,weighting))
        for devsux in devinfosux:
            weighting -= 1
            logger.debug("Credential %s, Counted Successful DeviceInfo record, Weighting Updated: %s"%(label,weighting))
        for credfail in credfails:
            weighting += 1
            logger.debug("Credential %s, Counted Failed record, Weighting Updated: %s"%(label,weighting))

        cred_weighting.append({"uuid":cred.get('uuid'),"weighting":weighting})
        logger.debug("Credential %s, Final Weighting: %s"%(label,weighting))

    weighted = sorted(cred_weighting, key=lambda k: k['weighting'])
    logger.debug("Sorted weights: %s"%(weighted))
    index = 0

    for weighted_cred in weighted:
        weighted_cred.update({"index":index})
        index += 1
        logger.debug("Indexing: %s"%(weighted_cred))
    
    print("\nOrdering credentials...\n")

    data = []

    if apply:
        for weighted_cred in weighted:
            logger.debug("Updating: %s" % (weighted_cred))
            headers = ["New Index", "Credential", "Scope", "Outpost URL"]
            creds.update_cred(
                weighted_cred.get("uuid"), {"index": weighted_cred.get("index")}
            )
    else:
        headers = [
            "Credential",
            "Current Index",
            "Weighting",
            "New Index",
            "Scope",
            "Outpost URL",
        ]
        for cred in credlist:
            for weighted_cred in weighted:
                logger.debug(
                    "Evaluating: %s ... %s" % (cred.get("uuid"), weighted_cred.get("uuid"))
                )
                if cred.get("uuid") == weighted_cred.get("uuid"):
                    index = cred.get("index")
                    label = cred.get("label")
                    weight = weighted_cred.get("weighting")
                    new_index = weighted_cred.get("index")
                    scope = cred.get("scopes") or []
                    if isinstance(scope, list):
                        scope = ", ".join(scope)
                    url = outpost_map.get(cred.get("uuid"))
                    msg = "%s: Index: %s, Weight: %s, New Index: %s" % (
                        label,
                        index,
                        weight,
                        new_index,
                    )
                    logger.info(msg)
                    data.append([label, index, weight, new_index, scope, url])

    # Refresh
    credlist = api.get_json(creds.get_vault_credentials)
    msg = "New Credential Order:\n"
    print(msg)
    logger.info(msg)
    for cred in credlist:
        label = cred.get("label")
        index = cred.get("index")
        msg = "%s) %s" % (index, label)
        logger.info(msg)
        # Previously, refresh data was appended to ``data`` here which resulted
        # in the report containing rows without weighting or new index values.
        # Only log the new order to avoid mixing datasets.

    if data:
        # Prepend the discovery instance before exporting the report.
        headers.insert(0, "Discovery Instance")
        for row in data:
            row.insert(0, getattr(args, "target", None))

    # Export the suggested credential optimisation report using the new
    # ``suggested_cred_opt`` key so downstream consumers and the CLI can
    # reference a consistent name.
    output.report(data, headers, args, name="suggested_cred_opt")

def get_device(search, credentials, args):
    dev = args.excavate[1]
    msg = "\nDevice Lookup: %s" % dev
    logger.info(msg)
    print(msg)

    devJSON = {
                "query":
                "search flags(no_segment) Host, NetworkDevice, Printer, SNMPManagedDevice, StorageDevice, ManagementController where name = '%s' show name, os, kind(#) as 'nodekind'" % dev
               }
    logger.debug("Executing device search query for %s: %s", dev, devJSON.get("query"))
    dev_resp = search.search(devJSON,format="object")
    logger.debug("Device search HTTP status: %s", getattr(dev_resp, "status_code", "n/a"))
    devResults = api.get_json(dev_resp)
    devTotal = 0
    if not devResults or not isinstance(devResults, list):
        logger.error("Failed to retrieve device lookup results")
    elif len(devResults) > 0 and isinstance(devResults[0], dict):
        devTotal = devResults[0].get('count', 0)
    logger.debug("Devices Total: %s"%(devTotal))

    if devTotal > 0:
        first = devResults[0]
        if isinstance(first, dict) and first.get('results'):
            os = first['results'][0].get('os')
            kind = first['results'][0].get('nodekind')
            msg = "\nNodekind: %s\nOperating System: %s\n" % (kind, os)
            logger.info(msg)
            print(msg)
    else:
        msg = "\nDevice not found!\n"
        logger.warning(msg)
        print(msg)

    qryJSON = {
                "query":
                """search flags(no_segment) Host, NetworkDevice, Printer, SNMPManagedDevice, StorageDevice, ManagementController where name = '%s'
                   traverse InferredElement:Inference:Associate:DiscoveryAccess
                   traverse DiscoveryAccess:Metadata:Detail:SessionResult
                   show
                   session_type as 'session_type',
                   credential as 'credential',
                   success as 'success',
                   message as 'message',
                   kind(#) as 'nodekind'""" % dev
               }
    sessionResults = api.search_results(search,qryJSON)
    total = len(sessionResults)
    failed = False
    logger.debug("Session Results Total: %s"%(total))
    if total == 0:
        # Alternate lookup
        qryJSON = {
                    "query":
                    """search flags(no_segment) Host, NetworkDevice, Printer, SNMPManagedDevice, StorageDevice, ManagementController where name = '%s'
                       traverse InferredElement:Inference:Associate:DiscoveryAccess
                       traverse DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo
                       show
                       last_access_method as 'session_type',
                       (last_credential or last_slave) as 'credential',
                       method_success as 'success',
                       'Credential ID Retrieved from DeviceInfo' as 'message',
                       kind(#) as 'nodekind'""" % dev
                   }
        sessionResults = api.search_results(search,qryJSON)
        total = len(sessionResults)
        logger.debug("Alternate Session Results Total: %s"%(total))
        if total == 0:
            failed = True
            if devTotal > 0:
                missing = "DiscoveryAccess may have aged out or no session results.\n"
            else:
                missing = "Device not found or DiscoveryAccess may have aged out.\n"

    # Build the results
    
    data = []
    if failed:
        logger.warning(missing)
        print(missing)

    uuid = None

    for result in sessionResults:
        logger.debug("Processing Result: %s"%(result))
        uuid = result['credential']
        status = None
        label = None
        username = None
        if uuid:
            vaultcreds = api.get_json(credentials.listCredentials(uuid))
            cred_detail = get_credentials(vaultcreds)
            logger.debug("Credential retrieved: %s"%(cred_detail))
            label = cred_detail.get('label')
            enabled = cred_detail.get('enabled')
            username = cred_detail.get('username')
            if enabled:
                status = "Enabled"
            else:
                status = "Disabled"
        st = result['session_type']
        c = label
        ci = uuid
        m = result['message']
        s = result['success']
        data.append([ st, c, ci, username, status, m, s ])

    output.report(data,
                        [
                            "Session Type",
                            "Credential",
                            "Credential ID",
                            "Credential Login",
                            "Status",
                            "Message",
                            "Successful"
                            ], args, name="device")

def scheduling(vault, search, args):
    ## Schedules compared to runs
    print("\nScheduled Runs with Credentials")
    print("-------------------------------")
    logger.info("Running Schedules Report...")
    print("Running Schedules Report...")
    msg = None

    heads = ["Name", "Type", "Range ID", "Ranges", "Scan Level", "When", "Credentials"]
    data = []

    vaultcreds = api.get_json(vault.get_vault_credentials)
    if not vaultcreds or not isinstance(vaultcreds, list):
        logger.error("Vault credentials could not be retrieved")
        output.report([], heads, args, name="schedules")
        return

    credential_ips = []
    timer_count = 0
    for cred in vaultcreds:
        timer_count = tools.completage("Getting credentials...", len(vaultcreds), timer_count)
        logger.debug("Getting detail for credential %s"%cred)
        detail = get_credentials(cred)
        list_of_ips = []
        uuid = detail.get('uuid')
        label = detail.get('label')
        if detail.get("iprange"):
            list_of_ips = tools.range_to_ips(detail.get('iprange'))
            logger.debug("%s IP Range: %s"%(cred,list_of_ips))
        credential_ips.append([uuid,list_of_ips,label])
    print(os.linesep,end="\r")

    logger.debug("Executing excludes query: %s", queries.excludes)
    excludes_resp = search.search(queries.excludes,format="object")
    logger.debug("Excludes search HTTP status: %s", getattr(excludes_resp, "status_code", "n/a"))
    excludes = api.get_json(excludes_resp)
    data = []
    if excludes is None or not isinstance(excludes, list):
        logger.error("Failed to retrieve excludes")
        output.report(data, heads, args, name="schedules")
        return
    if len(excludes) == 0:
        msg = "No exclude ranges found"
        logger.info(msg)
        print(msg)
        results = {"results": []}
    else:
        results = excludes[0]
        if not isinstance(results, dict) or 'results' not in results:
            logger.error("Invalid excludes result structure")
            output.report(data, heads, args, name="schedules")
            return
    exclude_ips = []

    timer_count = 0
    for result in results.get('results'):
        timer_count = tools.completage("Processing excludes...", len(results.get('results')), timer_count)
        logger.debug("Processing Exclude result %s"%(result))
        r = result['Scan_Range'][0]
        fr = result.get('Scan_Range')
        i = result.get('ID')
        sc = result.get('Label')
        dr = result.get('Date_Rules')
        list_of_ips = tools.range_to_ips(r)
        exclude_ips.append([i,list_of_ips])

        in_exclude = []

        for run in exclude_ips:
            logger.debug("Processing Exclude Run %s"%(run))
            run_ips = run[1]
            for credential in credential_ips:
                cred_ips = credential[1]
                for cred_ip in cred_ips:
                    if isinstance(cred_ip, (ipaddress.IPv4Network, ipaddress.IPv6Network)):
                        if any(
                            isinstance(run_ip, (ipaddress.IPv4Network, ipaddress.IPv6Network))
                            and cred_ip.overlaps(run_ip)
                            for run_ip in run_ips
                        ):
                            logger.debug("Credential IP %s found in Exclude run"%(cred_ip))
                            in_exclude.append("%s (%s)" % (credential[2],credential[0]))
                    elif cred_ip == "0.0.0.0/0,::/0" and "0.0.0.0/0,::/0" in run_ips:
                        in_exclude.append("%s (%s)" % (credential[2],credential[0]))
        in_exclude = tools.sortlist(in_exclude)
        logger.debug("Excludes:%s"%(in_exclude))

        range_count = len(fr or [])
        cred_count = len(in_exclude)
        if args.output_csv or args.output_file:
            msg = os.linesep
        else:
            msg = (
                "\nOnly showing ranges, credential counts for tables output. "
                "Output to CSV for credential list.\n"
            )
        data.append([sc, "Exclude Range", i, range_count, None, dr, cred_count])
    if timer_count > 0:
        print(os.linesep,end="\r")
    
    logger.debug("Executing scan range query: %s", queries.scanrange.get("query", queries.scanrange))
    scan_resp = search.search(queries.scanrange,format="object")
    logger.debug("Scan range search HTTP status: %s", getattr(scan_resp, "status_code", "n/a"))
    scan_ranges = api.get_json(scan_resp)
    if scan_ranges is None or not isinstance(scan_ranges, list):
        logger.error("Failed to retrieve scan ranges")
        output.report(data, heads, args, name="schedules")
        return
    if len(scan_ranges) == 0:
        msg = "No scan ranges found"
        logger.info(msg)
        print(msg)
        results = {"results": []}
    else:
        first = scan_ranges[0]
        if isinstance(first, dict) and 'results' in first:
            results = first
        else:
            results = {"results": scan_ranges}

    range_ips = []
    timer_count = 0
    for result in results['results']:
        timer_count = tools.completage("Processing runs...", len(results['results']), timer_count)
        logger.debug("Processing Scan range:%s"%(result))
        r = result['Scan_Range'][0]
        fr = result.get('Scan_Range')
        i = result.get('ID')
        sc = result.get('Label')
        sl = result.get('Level')
        dr = result.get('Date_Rules')
        list_of_ips = tools.range_to_ips(r)
        range_ips.append([i,list_of_ips])

        in_run = []

        for run in range_ips:
            logger.debug("Processing Run %s"%(run))
            run_ips = run[1]
            for credential in credential_ips:
                cred_ips = credential[1]
                for cred_ip in cred_ips:
                    if isinstance(cred_ip, (ipaddress.IPv4Network, ipaddress.IPv6Network)):
                        if any(
                            isinstance(run_ip, (ipaddress.IPv4Network, ipaddress.IPv6Network))
                            and cred_ip.overlaps(run_ip)
                            for run_ip in run_ips
                        ):
                            in_run.append("%s (%s)" % (credential[2],credential[0]))
                            logger.debug("Credential IP %s found in run"%(cred_ip))
                    elif cred_ip == "0.0.0.0/0,::/0":
                        in_run.append("%s (%s)" % (credential[2],credential[0]))
                        logger.debug("No range specified - scan all - %s"%(cred_ip))
        in_run = tools.sortlist(in_run)
        logger.debug("Runs:%s"%(in_run))
        
        range_count = len(fr or [])
        cred_count = len(in_run)
        if args.output_csv or args.output_file:
            msg = os.linesep
        else:
            msg = (
                "\nOnly showing ranges, credential counts for tables output. "
                "Output to CSV for credential list.\n"
            )
        data.append([sc, "Scan Range", i, range_count, sl, dr, cred_count])
    print(os.linesep,end="\r")

    # sort data by index field
    data.sort(key=lambda x: x[2])

    if msg:
        print(msg)

    output.report(data, heads, args, name="schedules")

def unique_identities(
    search,
    include_endpoints=None,
    endpoint_prefix=None,
    max_endpoints=None,
):
    """Return a list of unique device identities.

    This routine queries the appliance using the ``device_ids`` lookup
    which returns discovery access records with associated identity
    details.  The result set is processed to collate IP addresses and
    hostnames into unique identity groupings.

    Parameters
    ----------
    search: object
        API search handle.
    include_endpoints: list[str] | None
        Explicit list of endpoint IPs to include.  If provided, only these
        endpoints are processed.
    endpoint_prefix: str | None
        Optional prefix that endpoints must start with.  Ignored when
        ``include_endpoints`` is supplied.
    max_endpoints: int | None
        Optional limit for the number of endpoints to process.  When provided
        the loop over devices stops once this many unique endpoints have been
        encountered.
    """

    cache_key = {"include_endpoints": include_endpoints, "endpoint_prefix": endpoint_prefix}
    if cache.is_enabled():
        cached = cache.load("unique_identities", cache_key, 0)
        if cached is not None:
            return cached

    logger.info("Running: Unique Identities report...")
    print("Running: Unique Identities report...")

    # Retrieve discovery access information along with associated identity
    # fields.  The result set is optionally constrained to a subset of
    # endpoints to reduce the amount of data returned from the API.
    query = queries.device_ids
    if include_endpoints:
        endpoint_filter = ",".join(f"'{ep}'" for ep in include_endpoints)
        query = query.replace(
            "search DiscoveryAccess",
            f"search DiscoveryAccess where endpoint in ({endpoint_filter})",
        )
    elif endpoint_prefix:
        query = query.replace(
            "search DiscoveryAccess",
            f"search DiscoveryAccess where endpoint beginswith '{endpoint_prefix}'",
        )

    access_results = api.search_results(
        search, query, cache_name="unique_identities_device_ids"
    )
    if not isinstance(access_results, list):
        logger.error("Failed to retrieve unique identity data")
        return []

    def _endpoint_in_scope(endpoint: str) -> bool:
        if not endpoint:
            return False
        if include_endpoints:
            return endpoint in include_endpoints
        if endpoint_prefix:
            return endpoint.startswith(endpoint_prefix)
        return True

    endpoint_map = {}

    # Fields to expand for IPs and hostnames
    ip_fields = [
        "DiscoveryAccess.endpoint",
        "Endpoint.endpoint",
        "DiscoveredIPAddress.ip_addr",
        "InferredElement.__all_ip_addrs",
        "NetworkInterface.ip_addr",
    ]
    name_fields = [
        "InferredElement.name",
        "InferredElement.hostname",
        "InferredElement.local_fqdn",
        "InferredElement.sysname",
        "NetworkInterface.fqdns",
    ]

    total_records = len(access_results)
    timer_count = 0

    for device in access_results:
        timer_count = tools.completage(
            f"Running: Unique Identities report... {timer_count + 1} record of {total_records}",
            total_records,
            timer_count,
        )
        if not isinstance(device, dict):
            logger.warning("Unexpected device record: %r", device)
            continue

        endpoint = tools.getr(device, "DiscoveryAccess.endpoint")
        if not _endpoint_in_scope(endpoint):
            continue

        ips = []
        names = []
        for field in ip_fields:
            ips = tools.list_of_lists(device, field, ips)
        for field in name_fields:
            names = tools.list_of_lists(device, field, names)

        ips_set = {ip for ip in ips if ip is not None}
        names_set = {name for name in names if name is not None}

        for ip in ips_set:
            data = endpoint_map.setdefault(ip, {"ips": set(), "names": set()})
            data["ips"].update(ips_set)
            data["names"].update(names_set)

        if max_endpoints and len(endpoint_map) >= max_endpoints:
            break

    if timer_count > 0:
        print(os.linesep, end="")

    unique_identities = []
    for endpoint, data in endpoint_map.items():
        ip_list = tools.sortlist(list(data["ips"]), "None") if data["ips"] else []
        name_list = (
            tools.sortlist(list(data["names"]), "None") if data["names"] else []
        )
        unique_identities.append(
            {
                "originating_endpoint": endpoint,
                "list_of_ips": ip_list,
                "list_of_names": name_list,
            }
        )

    if cache.is_enabled():
        cache.save("unique_identities", cache_key, 0, unique_identities)

    return unique_identities

def ip_analysis(tw_search, args):

    print("\nIP Analysis")
    print("-----------")
    logger.info("Running: IP analysis report...")
    print("Running: IP analysis report...")
    heads = ["IP Address", "Scan Schedules"]

    logger.debug("Executing scan range query: %s", queries.scanrange.get("query", queries.scanrange))
    scan_resp = tw_search.search(queries.scanrange, format="object")
    logger.debug("Scan range search HTTP status: %s", getattr(scan_resp, "status_code", "n/a"))
    scan_ranges = api.get_json(scan_resp)
    logger.debug("Raw scan range results: %s", scan_ranges)
    if isinstance(scan_ranges, dict):
        results = scan_ranges.get("results", [])
    elif isinstance(scan_ranges, list):
        if scan_ranges and isinstance(scan_ranges[0], dict) and "results" in scan_ranges[0]:
            results = scan_ranges[0].get("results", [])
        else:
            results = scan_ranges
    else:
        logger.error("Failed to retrieve scan ranges")
        output.report([], heads, args, name="ip_analysis")
        return

    if not isinstance(results, list):
        logger.error("Invalid scan range structure")
        output.report([], heads, args, name="ip_analysis")
        return

    if len(results) == 0:
        msg = "No scan ranges found"
        logger.info(msg)
        print(msg)

    logger.debug("Parsed %d scan range results", len(results))

    ip_to_ranges = defaultdict(set)
    scheduled_ip_set = set()

    timer_count = 0
    for result in results:
        timer_count = tools.completage(
            "Gathering Results...",
            len(results),
            timer_count,
        )
        logger.debug("Scan Result:\n%s", result)
        label = result.get('Label')
        for scan_range in result.get('Scan_Range'):
            nets = tools.range_to_ips(scan_range)
            logger.debug("List of Networks:%s", nets)
            for net in nets:
                net_str = str(net)
                ip_to_ranges[net_str].add(label)
                scheduled_ip_set.add(net_str)

    matched_runs = [
        {"ip": ip, "runs": sorted(list(labels))}
        for ip, labels in ip_to_ranges.items()
        if len(labels) > 1
    ]

    logger.debug("Executing excludes query: %s", queries.excludes)
    excludes_resp = tw_search.search(queries.excludes, format="object")
    logger.debug("Excludes search HTTP status: %s", getattr(excludes_resp, "status_code", "n/a"))
    excludes = api.get_json(excludes_resp)
    logger.debug("Raw exclude results: %s", excludes)
    if isinstance(excludes, dict):
        e_results = excludes.get("results", [])
    elif isinstance(excludes, list):
        if excludes and isinstance(excludes[0], dict) and "results" in excludes[0]:
            e_results = excludes[0].get("results", [])
        else:
            e_results = excludes
    else:
        logger.error("Failed to retrieve excludes")
        output.report([], heads, args, name="ip_analysis")
        return

    if not isinstance(e_results, list):
        logger.error("Invalid excludes result structure")
        output.report([], heads, args, name="ip_analysis")
        return

    if len(e_results) == 0:
        msg = "No exclude ranges found"
        logger.info(msg)
        print(msg)

    logger.debug("Parsed %d exclude results", len(e_results))

    for result in e_results:
        r = result['Scan_Range'][0]
        list_of_ips = tools.range_to_ips(r)
        logger.debug(
            "List of Exclude Ips to be added to Scheduled_ip_list: %s", list_of_ips
        )
        for ip in list_of_ips:
            scheduled_ip_set.add(str(ip))

    scheduled_ip_list = tools.sortlist(list(scheduled_ip_set))

    # Check for missing IPs
    missing_ips = []
    ip_schedules = api.search_results(tw_search, queries.ip_schedules)
    for ip_sched in ip_schedules:
        endpoint = tools.getr(ip_sched, 'endpoint')
        if endpoint not in scheduled_ip_set:
            missing_ips.append(endpoint)
            logger.debug("Missing endpoint: %s", endpoint)
    missing_ips = tools.sortlist(missing_ips)

    # Look for connections seen on the network but not yet scanned
    unscanned_results = api.search_results(
        tw_search, queries.connections_unscanned
    )

    data = []

    for matching in matched_runs:
        if len(matching.get("runs")) > 1:
            data.append([ matching.get("ip"), matching.get("runs") ])
            logger.debug("Matching Run: %s,%s"%(matching.get("ip"),matching.get("runs")))

    if len(data) == 0:
        msg = "No overlap between ranges."
        logger.info(msg)
        print(msg)
    matches = len(data)
    logger.debug("Matches:\n%s"%(matches))

    for missing_ip in missing_ips:
        data.append([ missing_ip, "Endpoint has previous DiscoveryAccess, but not currently scheduled." ])

    existing_ips = {row[0] for row in data}
    for unscanned in unscanned_results:
        unseen_ip = tools.getr(unscanned, 'Unscanned Host IP Address')
        if unseen_ip and unseen_ip not in existing_ips:
            data.append([ unseen_ip, "Seen but unscanned." ])
            existing_ips.add(unseen_ip)

    if len(data) == matches:
        msg = "No missing IPs in ranges."
        logger.info(msg)
        print(msg)

    output.report(data, heads, args, name="ip_analysis")


def overlapping(tw_search, args):
    """Compatibility wrapper for legacy overlapping report."""
    ip_analysis(tw_search, args)

def get_scans(results, list_of_ranges):
    """Return labels of scans that include any of ``list_of_ranges``.

    ``list_of_ranges`` is converted to a :class:`set` to avoid redundant
    comparisons. Each scan range is parsed into :mod:`ipaddress` network
    objects (with results cached by :func:`_range_to_networks`), and
    membership is evaluated using ``ip in network``.
    """
    scan_ranges = []
    if not results:
        return scan_ranges
    ip_set = set(list_of_ranges)
    for result in results:
        logger.debug("Result: %s", result)
        ranges = result.get('Scan_Range')
        if ranges and isinstance(ranges, list):
            for scan_range in ranges:
                logger.debug("Scan Range: %s", scan_range)
                r = scan_range
                label = result.get('Label')
                networks = _range_to_networks(r)
                logger.debug("List of Networks: %s", networks)
                for ip in list_of_ranges:
                    logger.debug("Checking IP %s in networks", ip)
                    if ip == "0.0.0.0/0,::/0":
                        scan_ranges.append(label)
                        logger.debug("IP %s added to scheduled_scans", ip)
                        continue

                    if isinstance(ip, (ipaddress.IPv4Network, ipaddress.IPv6Network)):
                        for net in networks:
                            if isinstance(net, (ipaddress.IPv4Network, ipaddress.IPv6Network)) and ip.overlaps(net):
                                scan_ranges.append(label)
                                logger.debug("IP %s added to scheduled_scans", ip)
                                break
                    else:
                        for net in networks:
                            if isinstance(net, (ipaddress.IPv4Network, ipaddress.IPv6Network)) and ip in net:
                                scan_ranges.append(label)
                                logger.debug("IP %s added to scheduled_scans", ip)
                                break
    scan_ranges = tools.sortlist(scan_ranges)
    return scan_ranges
