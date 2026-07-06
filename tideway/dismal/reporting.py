# DisMAL Reporting Functions

import datetime
import logging
from platform import uname
import os
from collections import Counter, defaultdict
import json
import re
from concurrent.futures import ThreadPoolExecutor
import csv

# PIP Packages
import pandas as pd

# Local
from . import api, queries, tools, builder, output, access, cli
import tideway

logger = logging.getLogger("_reporting_")

def chunked_search(
    search,
    base_query,
    chunks,
    *,
    limit=0,
    use_cache=True,
    cache_name="chunk",
    page_size=500,
):
    """Public wrapper for :func:`api.search_in_chunks`.

    This helper is exposed for CLI consumers that need to execute the same
    query repeatedly across multiple time windows or endpoint groups and
    receive a single merged result set.
    """

    return api.search_in_chunks(
        search,
        base_query,
        chunks,
        limit=limit,
        use_cache=use_cache,
        cache_name=cache_name,
        page_size=page_size,
    )

@output._timer("Success Report")
def successful(creds, search, args, max_workers=None):
    """Generate the credential success report.

    Parameters
    ----------
    creds, search, args
        Standard API helper objects passed in by ``dismal``.
    max_workers : int, optional
        Maximum number of worker threads for concurrent API queries.  When
        ``None`` (the default) this value is read from ``args.max_threads`` and
        falls back to ``2`` if unspecified.  A small default keeps load on the
        appliance conservative.
    """

    msg = "Running: Success Report )"
    logger.info(msg)

    vaultcreds = api.get_json(creds.get_vault_credentials)
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug('List Credentials: %s', json.dumps(vaultcreds))

    outpost_map = {}
    if getattr(args, "target", None) and hasattr(tideway, "appliance"):
        try:
            token = getattr(args, "token", None)
            if not token and getattr(args, "f_token", None):
                if os.path.isfile(args.f_token):
                    with open(args.f_token, "r") as f:
                        token = f.read().strip()
            app = tideway.appliance(args.target, token)
            outpost_map = api.get_outpost_credential_map(search, app)
            logger.debug("Outpost credential map: %s", outpost_map)
        except Exception as e:  # pragma: no cover - network errors
            logger.error("Failed to retrieve outpost credentials: %s", e)

    credsux_results = {}
    devinfosux = {}
    credfail_results = {}
    credsux7_results = {}
    devinfosux7 = {}
    credfail7_results = {}

    # Determine thread pool size.  Limit to at least one worker to avoid
    # runtime errors if an invalid value is supplied.
    if max_workers is None:
        max_workers = getattr(args, "max_threads", 2)
    try:
        max_workers = max(1, int(max_workers))
    except (TypeError, ValueError):  # pragma: no cover - defensive
        max_workers = 2

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            "credsux_results": executor.submit(
                api.search_results,
                search,
                queries.credential_success,
                0,
                True,
                "credential_success",
            ),
            "devinfosux": executor.submit(
                api.search_results,
                search,
                queries.deviceinfo_success,
                0,
                True,
                "deviceinfo_success",
            ),
            "credfail_results": executor.submit(
                api.search_results,
                search,
                queries.credential_failure,
                0,
                True,
                "credential_failure",
            ),
            "credsux7_results": executor.submit(
                api.search_results,
                search,
                queries.credential_success_7d,
                0,
                True,
                "credential_success_7d",
            ),
            "devinfosux7": executor.submit(
                api.search_results,
                search,
                queries.deviceinfo_success_7d,
                0,
                True,
                "deviceinfo_success_7d",
            ),
            "credfail7_results": executor.submit(
                api.search_results,
                search,
                queries.credential_failure_7d,
                0,
                True,
                "credential_failure_7d",
            ),
            "outpost_cred_results": executor.submit(
                api.search_results,
                search,
                queries.outpost_credentials,
                0,
                True,
                "outpost_credentials",
            ),
        }

        results = {}
        for key, future in futures.items():
            try:
                results[key] = future.result()
            except Exception as e:
                logger.error("Failed to retrieve %s: %s", key, e)
                results[key] = []

    credsux_results = results.get("credsux_results", [])
    devinfosux = results.get("devinfosux", [])
    credfail_results = results.get("credfail_results", [])
    credsux7_results = results.get("credsux7_results", [])
    devinfosux7 = results.get("devinfosux7", [])
    credfail7_results = results.get("credfail7_results", [])
    outpost_cred_results = results.get("outpost_cred_results", [])

    data = []
    headers = []

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug('Successful SessionResults: %s', json.dumps(credsux_results))
        logger.debug('Successful DeviceInfos: %s', json.dumps(devinfosux))
        logger.debug('Failures: %s', json.dumps(credfail_results))

    suxCreds = tools.session_get(credsux_results)
    suxDev = tools.session_get(devinfosux)
    failCreds = tools.session_get(credfail_results)
    suxCreds7 = tools.session_get(credsux7_results)
    suxDev7 = tools.session_get(devinfosux7)
    failCreds7 = tools.session_get(credfail7_results)

    # Build mapping of credential UUIDs to outpost IDs and URLs.
    cred_outposts = {}
    if isinstance(outpost_map, dict):
        for op_id, info in outpost_map.items():
            if not isinstance(info, dict):
                continue
            url = info.get("url")
            for cred in info.get("credentials", []) or []:
                cred_outposts.setdefault(str(cred), {})["id"] = str(op_id)
                if url:
                    cred_outposts[str(cred)]["url"] = url
    if isinstance(outpost_cred_results, dict):
        outpost_cred_results = outpost_cred_results.get("results", [])
    if isinstance(outpost_cred_results, list):
        for entry in outpost_cred_results:
            if not isinstance(entry, dict):
                continue
            uuid = entry.get("credential")
            op_id = entry.get("outpost")
            if uuid and op_id:
                info = cred_outposts.setdefault(str(uuid), {})
                info.setdefault("id", str(op_id))
                if outpost_map:
                    url = outpost_map.get(str(op_id), {}).get("url")
                    if url and not info.get("url"):
                        info["url"] = url

    # Include Scan Ranges and Excludes
    scan_ranges = api.search_results(
        search, queries.scanrange, limit=0, cache_name="scanrange"
    )
    if isinstance(scan_ranges, dict):
        scan_ranges_results = scan_ranges.get("results", [])
    else:
        scan_ranges_results = scan_ranges or []

    excludes = api.search_results(
        search, queries.excludes, limit=0, cache_name="excludes"
    )
    if isinstance(excludes, dict):
        excludes_results = excludes.get("results", [])
    else:
        excludes_results = excludes or []

    timer_count = 0
    for cred in vaultcreds:
        timer_count = tools.completage(
            "Gathering Credentials", len(vaultcreds), timer_count
        )

        logger.debug("Analysing Credential:%s", cred.get('uuid'))

        detail = builder.get_credentials(cred)

        uuid = detail.get('uuid')
        if uuid is not None:
            # Mirror the normalization performed in ``tools.session_get`` so
            # that dictionary lookups are case-insensitive and unaffected by
            # object-path prefixes such as "Credential/".
            uuid = str(uuid).split('/')[-1].lower()
        msg = "Working UUID :%s\n"%uuid
        logger.debug(msg)
        # Ensure index is numeric for downstream calculations
        index = int(tools.getr(detail, 'index', 0) or 0)
        
        ip_range = tools.getr(detail,'iprange',None)
        list_of_ranges = tools.range_to_ips(ip_range)
        ip_exclude = tools.getr(detail,'exclusions',None)
        enabled = tools.getr(detail,'enabled')
        if enabled:
            status = "Enabled"
        else:
            status = "Disabled"

        active = False
        success_all = 0
        fails_all = 0
        success7 = 0
        fails7 = 0
        session = None
        percent_all = 0.0
        percent7 = 0.0

        # Look up success/failure information for this credential
        sessions = suxCreds.get(uuid, [None, None])
        logger.debug("UUID %s -> sessions=%s", uuid, sessions)

        devinfos = suxDev.get(uuid, [None, None])
        logger.debug("UUID %s -> devinfos=%s", uuid, devinfos)

        failure = failCreds.get(uuid, [None, None])
        logger.debug("UUID %s -> failure=%s", uuid, failure)

        sessions7 = suxCreds7.get(uuid, [None, None])
        logger.debug("UUID %s -> sessions7=%s", uuid, sessions7)

        devinfos7 = suxDev7.get(uuid, [None, None])
        logger.debug("UUID %s -> devinfos7=%s", uuid, devinfos7)

        failure7 = failCreds7.get(uuid, [None, None])
        logger.debug("UUID %s -> failure7=%s", uuid, failure7)

        # Determine if this credential was seen in any query results, even if
        # the count is zero
        active = any(
            uuid in mapping
            for mapping in [
                suxCreds,
                suxDev,
                failCreds,
                suxCreds7,
                suxDev7,
                failCreds7,
            ]
        )
        active = active or any(
            count is not None
            for _, count in [
                sessions,
                devinfos,
                failure,
                sessions7,
                devinfos7,
                failure7,
            ]
        )
        logger.debug("UUID %s -> active=%s", uuid, active)

        if sessions[0] and devinfos[0]:
            success_all = int(sessions[1]) + int(devinfos[1])
            session = sessions[0] or devinfos[0]
            logger.debug("Sessions and DevInfos: %s", success_all)
        elif sessions[0]:
            # Successful sessions without device info results
            success_all = int(sessions[1])
            session = sessions[0]
            logger.debug("Sessions only: %s", success_all)
        elif devinfos[0]:
            # Device info successes only
            success_all = int(devinfos[1])
            session = devinfos[0]
            logger.debug("DevInfos only: %s", success_all)

        if sessions7[0] and devinfos7[0]:
            success7 = int(sessions7[1]) + int(devinfos7[1])
            logger.debug(
                "UUID %s -> success7=%s (sessions7 + devinfos7)", uuid, success7
            )
        elif sessions7[0]:
            success7 = int(sessions7[1])
            logger.debug("UUID %s -> success7=%s (sessions7 only)", uuid, success7)
        elif devinfos7[0]:
            success7 = int(devinfos7[1])
            logger.debug("UUID %s -> success7=%s (devinfos7 only)", uuid, success7)
        else:
            logger.debug("UUID %s -> success7=%s (no data)", uuid, success7)

        scheduled_scans = builder.get_scans(scan_ranges_results, list_of_ranges)
        logger.debug("Scheduled Scans List %s", scheduled_scans)

        excluded_scans = builder.get_scans(excludes_results, list_of_ranges)
        logger.debug("Excluded Scans List %s", excluded_scans)

        fails_all = int(failure[1] or 0)
        if fails_all:
            logger.debug("Failures:%s", fails_all)
        fails7 = int(failure7[1] or 0)

        # Mark credential as active when any failure data exists so the
        # reporting row is emitted with numeric zeros instead of being
        # considered unused.
        if failure[1] or failure7[1]:
            active = True

        # Coerce success/fail counts to ints and compute percentage as float
        success_all = int(success_all)
        fails_all = int(fails_all)
        total = success_all + fails_all
        if total > 0:
            logger.debug("Success:%s Total:%s", success_all, total)
            percent_all = success_all / float(total)

        success7 = int(success7)
        fails7 = int(fails7)
        total7 = success7 + fails7
        if total7 > 0:
            percent7 = success7 / float(total7)

        msg = None
        outpost_info = cred_outposts.get(uuid, {})
        outpost_id = outpost_info.get("id")
        outpost_url = outpost_info.get("url")
        usage = detail.get('usage')
        if args.output_file or args.output_csv:
            if active:
                data.append([
                    detail.get('label'),
                    index,
                    uuid,
                    detail.get('username'),
                    session or failure[0],
                    success_all,
                    fails_all,
                    percent_all,
                    percent7,
                    status,
                    usage,
                    ip_range,
                    ip_exclude,
                    scheduled_scans if scheduled_scans else None,
                    excluded_scans if excluded_scans else None,
                    outpost_id,
                    outpost_url,
                ])
            else:
                data.append([
                    detail.get('label'),
                    index,
                    uuid,
                    detail.get('username'),
                    detail.get('types'),
                    0,
                    0,
                    0.0,
                    0.0,
                    "Credential appears to not be in use (%s)" % status,
                    usage,
                    ip_range,
                    ip_exclude,
                    scheduled_scans if scheduled_scans else None,
                    excluded_scans if excluded_scans else None,
                    outpost_id,
                    outpost_url,
                ])
            headers = [
                "Credential",
                "Index",
                "UUID",
                "Login ID",
                "Protocol",
                "Successes",
                "Failures",
                "Success % All Time",
                "Success % 7 Days",
                "State",
                "Usage",
                "Ranges",
                "Excludes",
                "Scheduled Scans",
                "Exclusion Lists",
                "Outpost",
                "Outpost URL",
            ]
        else:
            if active:
                data.append([
                    detail.get('label'),
                    index,
                    uuid,
                    detail.get('username'),
                    session or failure[0],
                    success_all,
                    fails_all,
                    percent_all,
                    percent7,
                    status,
                    usage,
                    outpost_id,
                    outpost_url,
                ])
            else:
                data.append([
                    detail.get('label'),
                    index,
                    uuid,
                    detail.get('username'),
                    detail.get('types'),
                    0,
                    0,
                    0.0,
                    0.0,
                    "Credential appears to not be in use (%s)" % status,
                    usage,
                    outpost_id,
                    outpost_url,
                ])
            headers = [
                "Credential",
                "Index",
                "UUID",
                "Login ID",
                "Protocol",
                "Successes",
                "Failures",
                "Success % All Time",
                "Success % 7 Days",
                "State",
                "Usage",
                "Outpost",
                "Outpost URL",
            ]
    print(os.linesep,end="\r")

    if data:
        headers = list(dict.fromkeys(headers))
        headers.insert(0, "Discovery Instance")
        for row in data:
            row.insert(0, getattr(args, "target", None))

    if msg:
        print(msg)
    output.report(data, headers, args, name="credential_success")

@output._timer("Success Report (CLI)")
def successful_cli(client, args, sysuser, passwd, reporting_dir):
    credentials = access.remote_cmd('tw_vault_control --show --json -u %s -p %s'%(sysuser,passwd),client)
    credjson = []
    for cred in credentials.split("\n"):
        try:
            credjson.append(json.loads(cred))
        except:
            pass

    data = []
    headers = []

    for cred_detail in credjson:
        logger.debug("Analysing Credential: %s", cred_detail.get('uuid'))

        detail = tools.extract_credential(cred_detail)
        uuid = detail.get('uuid')
        
        list_of_ranges = detail.get('iprange')
        ip_exclude = detail.get('exclusions')
        enabled = tools.getr(detail,'enabled')
        types = tools.getr(detail,'types')
        if enabled:
            status = "Enabled"
        else:
            status = "Disabled"

        active = False
        success = 0
        failure = 0

        def _sum_for_uuid(csv_text, cred_uuid):
            total = 0
            reader = csv.DictReader(csv_text.splitlines())
            for row in reader:
                field = row.get("SessionResult.credential_or_slave") or row.get(
                    "SessionResult.slave_or_credential"
                ) or row.get("DeviceInfo.last_credential")
                if field and field.split("/")[-1] == cred_uuid:
                    try:
                        total += int(row.get("Count", 0) or 0)
                    except (TypeError, ValueError):
                        continue
            return total

        credsux = access.remote_cmd(
            'tw_query -u %s -p %s --csv %s'
            % (sysuser, passwd, queries.credential_success),
            client,
        )
        devinfosux = access.remote_cmd(
            'tw_query -u %s -p %s --csv %s'
            % (sysuser, passwd, queries.deviceinfo_success),
            client,
        )
        credfail = access.remote_cmd(
            'tw_query -u %s -p %s --csv %s'
            % (sysuser, passwd, queries.credential_failure),
            client,
        )

        success = _sum_for_uuid(credsux, uuid) + _sum_for_uuid(devinfosux, uuid)
        failure = _sum_for_uuid(credfail, uuid)
        active = success > 0 or failure > 0

        logger.debug("Failures found, Active: %s", failure)
            
        total = success + failure
        percent = 0.0
        if total > 0:
            logger.debug("Successes: %s Out of Total: %s", success, total)
            percent = success / total

        if active:
            logger.debug("UUID %s found Active", uuid)
            data.append([ detail.get('label'), uuid, detail.get('username'), types, success, failure, percent, status, list_of_ranges, ip_exclude ])
        else:
            logger.debug("UUID %s found Inactive", uuid)
            data.append([ detail.get('label'), uuid, detail.get('username'), types, None, None, 0.0, "Credential appears to not be in use (%s)" % status, detail.get('usage'), detail.get('internal_store'), list_of_ranges, ip_exclude ])
        headers = [ "Credential", "UUID", "Login ID", "Protocol", "Successes", "Failures", "Success %", "State", "Usage", "Store", "Scan Ranges", "Exclude Ranges" ]

    headers = list(dict.fromkeys(headers))
    headers.insert(0,"Discovery Instance")
    for row in data:
        row.insert(0, args.target)
    # Respect --preserve-existing during excavation runs
    cred_out = os.path.join(reporting_dir, "credentials.csv")
    try:
        if (
            getattr(args, "preserve_existing", False)
            and getattr(args, "excavate", None) is not None
            and os.path.exists(cred_out)
        ):
            msg = f"Preserving existing report: {cred_out}"
            print(msg)
            logger.info(msg)
        else:
            output.csv_file(data, headers, cred_out)
    except Exception:
        # Fall back to writing if any attribute checks fail
        output.csv_file(data, headers, cred_out)

@output._timer("Device Access Analysis")
def devices(twsearch, twcreds, args, identities=None):
    """Generate the device access report.

    The report previously relied on a monolithic query returning all device
    details.  To reduce load and support reuse elsewhere, the workflow now
    executes three granular queries (base, access, and network) and merges the
    results by ``DiscoveryAccess.endpoint`` before processing.
    """

    print("\nDevice Access Analyis")
    print("---------------------")
    logger.info("Running Data Analysis Report...")
    print("Running Data Analysis Report...")

    vaultcreds = api.get_json(twcreds.get_vault_credentials)

    # ``identities`` may be supplied by the caller to avoid recomputing the
    # expensive lookup when multiple reports need the same data.  Fall back to
    # gathering the identities here when not provided.
    if identities is None:
        identities = builder.unique_identities(
            twsearch,
            args.include_endpoints,
            args.endpoint_prefix,
            getattr(args, "max_identities", None),
        )

    # Gather device information using granular queries and merge by endpoint.
    # ``search_results`` defaults to returning at most 500 rows which can leave
    # many devices missing their base metadata (kind, last credential, access
    # method) when more are present.  Request all available rows for each query
    # to ensure subsequent merging has the necessary data for every device.
    base_results = api.search_results(twsearch, queries.deviceInfo_base, limit=0)
    access_results = api.search_results(twsearch, queries.deviceInfo_access, limit=0)
    network_results = api.search_results(twsearch, queries.deviceInfo_network, limit=0)

    merged = {}
    for result in base_results:
        if not isinstance(result, dict):
            continue
        ep = tools.getr(result, "DiscoveryAccess.endpoint", None)
        if ep:
            merged[ep] = result.copy()

    for dataset in (access_results, network_results):
        for result in dataset:
            if not isinstance(result, dict):
                continue
            ep = tools.getr(result, "DiscoveryAccess.endpoint", None)
            if not ep:
                continue
            entry = merged.setdefault(ep, {})
            entry.update(result)

    results = list(merged.values())

    # Track progress for identities and device results separately to avoid
    # nested progress collisions.  ``identity_timer`` counts completed
    # identities while ``result_timer`` tracks processed device results.
    total_result_iterations = len(results) * len(identities)
    identity_timer = 0
    result_timer = 0

    def _progress(id_done, id_total, res_done, res_total):
        """Display progress for identities and device results."""
        id_pct = (id_done / id_total) * 100 if id_total else 100
        res_pct = (res_done / res_total) * 100 if res_total else 100
        msg = (
            f"Gathering Device Results...: {id_pct:.0f}% | "
            f"Processing device results…: {res_pct:.0f}%"
        )
        print(f"\r{msg}", end="")

    devices = []
    msg = None
    headers = []

    # Build the results

    for identity in identities:
        identity_timer += 1
        _progress(identity_timer, len(identities), result_timer, total_result_iterations)
        logger.debug("Processing identity %s", identity)
        latest_timestamp = None
        all_credentials_used = []
        all_discovery_runs = []
        all_kinds = []
        device = {}
        last_identity = None
        last_scanned_ip = None
        last_kind = None
        for result in results:
            result_timer += 1
            _progress(identity_timer, len(identities), result_timer, total_result_iterations)
            da_endpoint = tools.getr(result,'DiscoveryAccess.endpoint',None)
            logger.debug("Checking endpoint %s in identity %s", da_endpoint, identity)

            # If this deviceinfo record relates to this device identity
            if da_endpoint in identity.get('list_of_ips'):

                # Collect ALL Data

                device_name = tools.getr(result,'DeviceInfo.hostname',"None")
                logger.debug("%s Device Name: %s", da_endpoint, device_name)
                all_device_names = [ device_name ]
                all_device_names = tools.list_of_lists(result,'Inferred_Name',all_device_names)
                all_device_names = tools.list_of_lists(result,'Inferred_Hostname',all_device_names)
                all_device_names = tools.list_of_lists(result,'Inferred_FQDN',all_device_names)
                all_endpoints = [ da_endpoint ]
                all_endpoints = tools.list_of_lists(result,'Endpoint.endpoint',all_endpoints)
                all_endpoints = tools.list_of_lists(result,'DiscoveredIPAddress.ip_addr',all_endpoints)
                all_endpoints = tools.list_of_lists(result,'InferredElement.__all_ip_addrs',all_endpoints)
                logger.debug("%s All endpoints: %s", da_endpoint, all_endpoints)
                    
                scan_run = tools.getr(result,'DiscoveryRun.label',"None")
                all_discovery_runs.append(scan_run)
                all_discovery_runs = tools.sortlist(all_discovery_runs)
                logger.debug("%s All Runs: %s", da_endpoint, all_discovery_runs)

                uuid = tools.getr(result,'DeviceInfo.last_credential',None)

                all_credentials_used = []
                cred_label = None
                cred_username = None
                if uuid:
                    credential_details = tools.get_credential(vaultcreds,uuid)
                    cred_label = tools.getr(credential_details,'label',"Not Found")
                    cred_username = tools.getr(credential_details,'username',"Not Found")
                    all_credentials_used.append("%s (%s)" % (cred_label,uuid))
                all_credentials_used = tools.sortlist(all_credentials_used)
                logger.debug("%s All Runs: %s", da_endpoint, all_credentials_used)
                
                da_result = tools.getr(result,'DiscoveryAccess.result',"None")
                end_state = tools.getr(result,'DiscoveryAccess.end_state',"None")
                last_marker = tools.getr(result,'DiscoveryAccess._last_marker',None)
                had_inference = tools.getr(result,'DiscoveryAccess.__had_inference',None)
                logger.debug("%s Last Marker: %s", da_endpoint, last_marker)
                logger.debug("%s Had Inference: %s", da_endpoint, had_inference)

                # Other Attributes

                first_marker = tools.getr(result,'DiscoveryAccess._first_marker',"None")
                last_interesting = tools.getr(result,'DiscoveryAccess._last_interesting',"None")
                os_type = tools.getr(result,'DeviceInfo.os_type',"None")
                device_type = tools.getr(result,'DeviceInfo.device_type',"None")
                method_success = tools.getr(result,'DeviceInfo.method_success',"None")
                method_failure = tools.getr(result,'DeviceInfo.method_failure',"None")
                endtime = tools.getr(result,'DiscoveryAccess.endtime',"None")
                kind = tools.getr(result,'DeviceInfo.kind',"None")
                last_access_method = tools.getr(result,'DeviceInfo.last_access_method',"None")
                logger.debug("%s Last Access Method: %s", da_endpoint, last_access_method)

                all_kinds.append(kind)

                start_time = tools.getr(result,'DiscoveryAccess.starttime',"None")

                device.update({
                                "all_device_names":identity.get('list_of_names'),
                                "all_endpoints":identity.get('list_of_ips'),
                                "all_credentials_used":all_credentials_used,
                                "all_discovery_runs":all_discovery_runs
                                })

                start_time_str = start_time.split(" ")
                start_time_str = start_time_str[:2]
                start_time_str = " ".join(start_time_str)
                start_timestamp = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
                logger.debug(
                    "%s Start Timestamp: %s latest Timestamp: %s",
                    da_endpoint,
                    start_timestamp,
                    latest_timestamp,
                )
                if not latest_timestamp or start_timestamp > latest_timestamp:
                    if not latest_timestamp:
                        logger.debug(
                            "%s No Latest Timestamp, setting to Start Timestamp: %s",
                            da_endpoint,
                            start_timestamp,
                        )
                    else:
                        logger.debug(
                            "%s Start Timestamp %s is fresher than latest_timestamp: %s",
                            da_endpoint,
                            start_timestamp,
                            latest_timestamp,
                        )
                    latest_timestamp = start_timestamp

                    if last_marker:
                        logger.debug("%s, %s Last Marker is set.", da_endpoint, latest_timestamp)
                    else:
                        logger.debug(
                            "%s, %s Last Marker missing.", da_endpoint, latest_timestamp
                        )

                    # Collect the very LAST Data

                    last_kind = kind
                    last_identity = device_name
                    last_scanned_ip = da_endpoint
                    last_credential = uuid
                    last_credential_label = cred_label
                    last_credential_username = cred_username
                    last_start_time = start_time
                    last_run = scan_run
                    last_endstate = end_state
                    last_result = da_result
                    last_access_method = last_access_method

                    device.update({
                                "last_identity":last_identity,
                                "last_kind":last_kind,
                                "last_scanned_ip":last_scanned_ip,
                                "last_credential":last_credential,
                                "last_credential_label":last_credential_label,
                                "last_credential_username":last_credential_username,
                                "last_start_time":last_start_time,
                                "last_run":last_run,
                                "last_endstate":last_endstate,
                                "last_result":last_result,
                                "last_access_method":last_access_method
                                })

                    if had_inference: # The last successful
                        logger.debug("%s, %s Had Inference.", da_endpoint, latest_timestamp)

                        last_successful_identity = device_name
                        last_successful_ip = da_endpoint
                        last_successful_credential = uuid
                        last_successful_credential_label = cred_label
                        last_successful_credential_username = cred_username
                        last_successful_start_time = start_time
                        last_successful_run = scan_run
                        last_successful_endstate = end_state
                        last_successful_result = da_result

                        device.update({
                                        "last_successful_identity":last_successful_identity,
                                        "last_successful_ip":last_successful_ip,
                                        "last_successful_credential":last_successful_credential,
                                        "last_successful_credential_label":last_successful_credential_label,
                                        "last_successful_credential_username":last_successful_credential_username,
                                        "last_successful_start_time":last_successful_start_time,
                                        "last_successful_run":last_successful_run,
                                        "last_successful_endstate":last_successful_endstate,
                                        "last_successful_result":last_successful_result,
                                        "last_access_method":last_access_method
                                        })
                
                if not last_identity:
                    last_identity = all_device_names[0]
                    device.update({"last_identity":last_identity})
                    logger.debug(
                        "%s, %s Last Identity missing, set to %s",
                        da_endpoint,
                        latest_timestamp,
                        last_identity,
                    )
                if not last_kind:
                    last_kind = kind
                    device.update({"last_kind":last_kind})
                    logger.debug(
                        "%s, %s Last Kind missing, set to %s",
                        da_endpoint,
                        latest_timestamp,
                        last_kind,
                    )
                if not last_scanned_ip:
                    last_scanned_ip = da_endpoint
                    device.update({"last_scanned_ip":last_scanned_ip})
                    logger.debug(
                        "%s, %s Last Scanned IP missing, set to %s",
                        da_endpoint,
                        latest_timestamp,
                        last_scanned_ip,
                    )

                devices.append(device)
                logger.debug("Device added to list of devices:%s", device)

    # Move to the next line after the progress output
    print()

    # Make sure we only report each device once - there is probably a more efficient way to do this in the loop.
    devices = list({v['last_identity']:v for v in devices}.values())
    logger.debug("Unique List of devices:%s", devices)

    # Build the report

    data = []

    for device in devices:
        last_scanned_ip = device.get("last_scanned_ip")
        last_identity = device.get('last_identity')
        last_kind = device.get('last_kind')
        all_device_names = device.get("all_device_names")
        all_endpoints = device.get("all_endpoints")
        all_credentials_used = device.get("all_credentials_used")
        all_discovery_runs = device.get("all_discovery_runs")
        last_credential = device.get("last_credential")
        last_credential_label = device.get("last_credential_label")
        last_credential_username = device.get("last_credential_username")
        last_start_time = device.get("last_start_time")
        last_run = device.get("last_run")
        last_endstate = device.get("last_endstate")
        last_result = device.get("last_result")
        last_successful_identity = device.get('last_successful_identity')
        last_successful_ip = device.get('last_successful_ip')
        last_successful_credential = device.get("last_successful_credential")
        last_successful_credential_label = device.get("last_successful_credential_label")
        last_successful_credential_username = device.get("last_successful_credential_username")
        last_successful_start_time = device.get("last_successful_start_time")
        last_successful_run = device.get("last_successful_run")
        last_successful_endstate = device.get("last_successful_endstate")
        last_access_method = device.get('last_access_method')

        msg = os.linesep
        if args.output_csv or args.output_file:    
            data.append([
                        last_scanned_ip,
                        last_identity,
                        last_kind,
                        all_device_names,
                        all_endpoints,
                        all_credentials_used,
                        all_discovery_runs,
                        last_credential,
                        last_credential_label,
                        last_credential_username,
                        last_start_time,
                        last_run,
                        last_endstate,
                        last_result,
                        last_access_method,
                        last_successful_identity,
                        last_successful_ip,
                        last_successful_credential,
                        last_successful_credential_label,
                        last_successful_credential_username,
                        last_successful_start_time,
                        last_successful_run,
                        last_successful_endstate,
                        ])
            headers = [
                    "last_scanned_ip",
                    "last_identity",
                    "last_kind",
                    "all_device_names",
                    "all_endpoints",
                    "all_credentials_used",
                    "all_discovery_runs",
                    "last_credential",
                    "last_credential_label",
                    "last_credential_username",
                    "last_start_time",
                    "last_run",
                    "last_endstate",
                    "last_result",
                    "last_access_method",
                    "last_successful_identity",
                    "last_successful_ip",
                    "last_successful_credential",
                    "last_successful_credential_label",
                    "last_successful_credential_username",
                    "last_successful_start_time",
                    "last_successful_run",
                    "last_successful_endstate"
                    ]
        else:
            msg = "\nOnly showing limited details for table output. Output to CSV for full results.\n"
            data.append([
                        last_scanned_ip,
                        last_identity,
                        last_kind,
                        last_credential_label,
                        last_start_time,
                        last_run,
                        last_endstate,
                        last_result,
                        last_access_method
                        ])

            headers = [
                    "last_scanned_ip",
                    "last_identity",
                    "last_kind",
                    "last_credential_label",
                    "last_start_time",
                    "last_run",
                    "last_endstate",
                    "last_result",
                    "last_access_method"
                    ]

    if msg:
        print(msg)
    output.report(data, headers, args, name="devices")

@output._timer("IP Address Lookup")
def ipaddr(search, credentials, args):
    ipaddr = args.excavate[1]
    msg = "\nIP Address Lookup: %s" % ipaddr
    logger.info(msg)
    print(msg)

    devices = {
                "query":
                """
                    search flags(no_segment) Host, NetworkDevice, Printer, SNMPManagedDevice, StorageDevice, ManagementController
                    where '%s' in __all_ip_addrs
                    show
                    name as 'Name',
                    os as 'OS',
                    kind(#) as 'Nodekind'
                    processwith unique()
                """ % ipaddr
               }
    accesses = {
                "query":
                """
                    search DiscoveryAccess where endpoint = '%s'
                    show
                    #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.hostname as 'DeviceInfo.hostname',
                    #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.device_type as 'DeviceInfo.device_type',
                    inferred_kind as 'nodekind',
                    (#DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.last_credential
                        or #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.last_slave) as 'DeviceInfo.last_credential',
                    #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.last_access_method as 'DeviceInfo.last_access_method',
                    #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.method_success as 'DeviceInfo.method_success',
                    'Credential ID Retrieved from DeviceInfo' as 'message'
                    process with unique()
                """ % ipaddr
               }

    devResults = api.search_results(search,devices)
    accessResults = api.search_results(search,accesses)
    # Use cached dropped endpoint data if available
    dropped = api.search_results(search, queries.dropped_endpoints)

    devices_found = []
    if len(devResults) == 1:
        msg = "\nDevices Found:"
        devices_found.append(devResults[0]['Name'])
        logger.debug("1 Dev Result: %s,%s", msg.strip(), devices_found)
    elif len(devResults) > 1:
        msg = "\nDevices Found:"
        for dev in devResults:
            devices_found.append(dev.get('Name'))
            logger.debug("Added Dev Result: %s", devices_found)
    if len(accessResults) == 1:
        msg = "\nDevices Found:"
        devices_found.append(accessResults[0]['Name'])
        logger.debug("1 DA result: %s,%s", msg.strip(), devices_found)
    elif len(accessResults) > 1:
        msg = "\nDevices Found:"
        for dev in accessResults:
            devices_found.append(dev.get('Name'))
            logger.debug("Added DA result: %s", devices_found)

    if len(devices_found) == 0:
        msg = "\nDevice not found or data may have aged out!"

        for drop in dropped:
            if drop.get('Endpoint') == ipaddr:
                msg = "Dropped IP Address"
                logger.debug("Endpoint %s is dropped IP", ipaddr)
    else:
        devices_found = tools.sortlist(devices_found)

    print(msg,devices_found,"\n")
    logger.debug("Unique List: %s,%s", msg.strip(), devices_found)

    id_list = []
    unique_ids = builder.unique_identities(
        search,
        args.include_endpoints,
        args.endpoint_prefix,
        getattr(args, "max_identities", None),
    )
    for identity in unique_ids:
        logger.debug("Checking IP address %s in Identity %s", ipaddr, identity)
        if ipaddr in identity.get('list_of_ips'):
            msg = "Identities Matched:"
            id_list.append(identity)
            logger.debug("Appending identity to list %s", identity)
    
    if len(id_list) > 0:
        print(msg)
        logger.info(msg)
        for id in id_list:
            print(id)
            logger.info(id)
        print(os.linesep)

    # Build the results
    
    data = []

    uuid = None

    sessionQry = {
                "query":
                """
                    search DiscoveryAccess where endpoint = '%s'
                    traverse DiscoveryAccess:Metadata:Detail:SessionResult
                    show
                    session_type as 'session_type',
                    credential as 'credential',
                    success as 'success',
                    message as 'message',
                    kind(#) as 'nodekind'
                    processwith unique()
                """ % ipaddr
               }
    sessionResults = api.search_results(search,sessionQry)
    total = len(sessionResults)
    logger.debug("%s Session results", total)
    if total == 0:
        # Alternate lookup
        sessionResults = accessResults
        total = len(sessionResults)
        logger.debug("%s Alternate Session results", total)

    # Build the results
    
    data = []

    uuid = None

    for result in sessionResults:
        uuid = result.get('credential')
        logger.debug("UUID from SessionResult %s", uuid)
        label = None
        username = None
        status = None
        if uuid:
            vaultcreds = api.get_json(credentials.get_vault_credential(uuid))
            logger.debug("Pulled Vault Credential %s", vaultcreds)
            detail = builder.get_credentials(vaultcreds)
            label = tools.getr(detail,'label')
            username = tools.getr(detail,'username')
            enabled = tools.getr(detail,'enabled')
            if enabled:
                status = "Enabled"
            else:
                status = "Disabled"
        st = result.get('session_type')
        m = result.get('message')
        s = result.get('success')
        data.append([ st, label, uuid, username, status, m, s ])

    output.report(
        data,
        [
            "Session Type",
            "Credential",
            "Credential ID",
            "Credential Login",
            "Status",
            "Message",
            "Successful",
        ],
        args,
    )




def chunked_last_disco(twsearch):
    """Return discovery access data by joining smaller query extracts.

    The historic :data:`core.queries.last_disco` query collected a very wide set
    of facts in a single TWQL statement.  That query is convenient but can be
    expensive for large environments.  This helper issues a series of more
    focused queries and stitches the results together using :mod:`pandas`.

    Parameters
    ----------
    twsearch : object
        Tideway search endpoint used for executing queries.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the merged discovery access information.
    """

    def _fetch_df(query, label, columns):
        """Return a DataFrame for ``query`` or an empty frame on error."""

        data = api.search_results(twsearch, query)
        if isinstance(data, list):
            if data:
                return pd.DataFrame(data)
            return pd.DataFrame(columns=columns)
        print(f"*** WARNING: {label} query failed; continuing with partial data. ***")
        return pd.DataFrame(columns=columns)

    # Retrieve foreign key mappings individually and merge on DiscoveryAccess.id
    device_keys = _fetch_df(
        queries.last_disco_key_deviceinfo,
        "DeviceInfo key",
        ["DiscoveryAccess.id", "DeviceInfo.id"],
    )
    if device_keys.empty:
        return device_keys
    run_keys = _fetch_df(
        queries.last_disco_key_run,
        "DiscoveryRun key",
        ["DiscoveryAccess.id", "DiscoveryRun.id"],
    )
    inferred_keys = _fetch_df(
        queries.last_disco_key_inferred,
        "InferredElement key",
        ["DiscoveryAccess.id", "InferredElement.id"],
    )
    session_keys = _fetch_df(
        queries.last_disco_key_session,
        "SessionResult key",
        ["DiscoveryAccess.id", "SessionResult.id"],
    )
    interface_keys = _fetch_df(
        queries.last_disco_key_interface,
        "NetworkInterface key",
        ["DiscoveryAccess.id", "NetworkInterface.id"],
    )

    key_df = device_keys.merge(run_keys, how="left", on="DiscoveryAccess.id")
    key_df = key_df.merge(inferred_keys, how="left", on="DiscoveryAccess.id")
    key_df = key_df.merge(session_keys, how="left", on="DiscoveryAccess.id")
    key_df = key_df.merge(interface_keys, how="left", on="DiscoveryAccess.id")

    access_df = _fetch_df(
        queries.last_disco_access,
        "DiscoveryAccess",
        [
            "DiscoveryAccess.id",
            "DiscoveryAccess.end_state",
            "DiscoveryAccess.previous_id",
            "DiscoveryAccess.next_id",
        ],
    )
    device_df = _fetch_df(
        queries.last_disco_deviceinfo,
        "DeviceInfo",
        [
            "DeviceInfo.id",
            "DeviceInfo.last_access_method",
            "DeviceInfo.last_slave",
            "DeviceInfo.probed_os",
        ],
    )
    run_df = _fetch_df(
        queries.last_disco_run,
        "DiscoveryRun",
        ["DiscoveryRun.id"],
    )
    session_df = _fetch_df(
        queries.last_disco_session,
        "SessionResult",
        [
            "SessionResult.id",
            "SessionResult.provider",
            "SessionResult.session_type",
            "SessionResult.success",
        ],
    )
    inferred_df = _fetch_df(
        queries.last_disco_inferred,
        "InferredElement",
        ["InferredElement.id", "InferredElement.__all_ip_addrs"],
    )
    interface_df = _fetch_df(
        queries.last_disco_interface,
        "NetworkInterface",
        ["NetworkInterface.id", "NetworkInterface.ip_addr"],
    )

    def _safe_search(query):
        try:
            return pd.DataFrame(api.search_results(twsearch, query))
        except api.APITimeoutError:
            logger.warning("Discovery API timed out; discovery report incomplete")
            return None

    key_df = _safe_search(queries.last_disco_functional_key)
    if key_df is None or key_df.empty:
        return pd.DataFrame()

    access_df = _safe_search(queries.last_disco_access)
    if access_df is None:
        return pd.DataFrame()
    device_df = _safe_search(queries.last_disco_deviceinfo)
    if device_df is None:
        return pd.DataFrame()
    run_df = _safe_search(queries.last_disco_run)
    if run_df is None:
        return pd.DataFrame()
    session_df = _safe_search(queries.last_disco_session)
    if session_df is None:
        return pd.DataFrame()
    inferred_df = _safe_search(queries.last_disco_inferred)
    if inferred_df is None:
        return pd.DataFrame()
    interface_df = _safe_search(queries.last_disco_interface)
    if interface_df is None:
        return pd.DataFrame()

    merged = key_df.merge(access_df, how="left", on="DiscoveryAccess.id")
    merged = merged.merge(device_df, how="left", on="DeviceInfo.id")
    merged = merged.merge(run_df, how="left", on="DiscoveryRun.id")
    if "SessionResult.id" in merged.columns:
        merged = merged.merge(session_df, how="left", on="SessionResult.id")
    if "InferredElement.id" in merged.columns:
        merged = merged.merge(inferred_df, how="left", on="InferredElement.id")
    if "NetworkInterface.id" in merged.columns:
        merged = merged.merge(interface_df, how="left", on="NetworkInterface.id")

    session_logged = merged.groupby("DiscoveryAccess.id")["SessionResult.provider"].transform(
        lambda s: s.isna().any()
    )
    merged["DiscoveryAccess.session_results_logged"] = session_logged

    if "DiscoveryAccess.end_state" in access_df.columns:
        prev_map = access_df.set_index("DiscoveryAccess.id")["DiscoveryAccess.end_state"]
    else:
        prev_map = pd.Series(dtype=object)
    merged["DiscoveryAccess.previous_end_state"] = merged["DiscoveryAccess.previous_id"].map(prev_map)

    merged["DiscoveryAccess.access_method"] = merged[
        "DeviceInfo.last_access_method"
    ].fillna(merged["SessionResult.session_type"])

    def _current_access(row):
        method = row.get("DeviceInfo.last_access_method")
        slave = row.get("DeviceInfo.last_slave")
        probed = row.get("DeviceInfo.probed_os")
        if method in ["windows", "rcmd"] and slave:
            return method
        if probed:
            return "Probe"
        return method

    merged["DiscoveryAccess.current_access"] = merged.apply(_current_access, axis=1)

    return merged


def _gather_discovery_data(twsearch, twcreds, args):
    """Return discovery access records without change analysis."""

    vaultcreds = api.get_json(twcreds.get_vault_credentials)
    identities = builder.unique_identities(
        twsearch,
        args.include_endpoints,
        args.endpoint_prefix,
        getattr(args, "max_identities", None),
    )
    # Retrieve discovery access information using chunked queries.  The
    # :func:`chunked_last_disco` helper returns a ``DataFrame`` containing the
    # merged facts from several smaller extracts.  Converting that frame into a
    # list of dictionaries keeps the remainder of this function compatible with
    # the previous implementation which operated on raw search results.
    df = chunked_last_disco(twsearch)
    if df.empty:
        logger.warning(
            "Discovery API timeouts were exhausted; discovery report incomplete"
        )
        discos = []
    else:
        discos = df.to_dict(orient="records")

    # Reuse cached dropped endpoint results if previously fetched
    dropped = api.search_results(twsearch, queries.dropped_endpoints)

    disco_data = []
    disco_by_endpoint = defaultdict(lambda: {"discos": [], "dropped": []})

    for result in discos:
        if not isinstance(result, dict):
            logger.warning("Unexpected discovery access entry: %r", result)
            continue
        endpoint = result.get("DiscoveryAccess.endpoint")
        if endpoint is None:
            continue
        disco_by_endpoint[endpoint]["discos"].append(result)
    for result in dropped:
        if not isinstance(result, dict):
            logger.warning("Unexpected dropped entry: %r", result)
            continue
        endpoint = result.get("Endpoint")
        if endpoint is None:
            continue
        disco_by_endpoint[endpoint]["dropped"].append(result)

    sorted_endpoints = tools.sortlist(list(disco_by_endpoint.keys()))

    # Build a lookup map so each endpoint can retrieve its identity without
    # repeatedly scanning the entire identity list.
    identity_map = {
        ip: identity
        for identity in identities
        for ip in identity.get("list_of_ips", [])
        if ip is not None
    }

    bins = [0, 59, 1440, 10080, 43830, 131487, 262974, 525949, 525950]
    labels = [
        "Less than 60 minutes ago",
        "Less than 24 hours ago",
        "Less than 7 days ago",
        "Less than 1 month ago",
        "Less than 3 months ago",
        "Less than 6 months ago",
        "Less than 12 months ago",
        "Over a year ago",
    ]

    timer_count = 0
    for endpoint in sorted_endpoints:
        timer_count = tools.completage(
            "Gathering Discovery Access Results...",
            len(sorted_endpoints),
            timer_count,
        )

        records = disco_by_endpoint[endpoint]

        end_states = [
            tools.getr(r, "DiscoveryAccess.end_state", None)
            for r in records["discos"]
        ] + [tools.getr(r, "End_State", None) for r in records["dropped"]]
        consistency = None
        if end_states:
            total = len(end_states)
            counter = dict(Counter(end_states))
            largest = max(counter, key=counter.get)
            if counter[largest] == total:
                consistency = f"Always {largest}"
            elif counter[largest] >= total - 2:
                consistency = f"Usually {largest}"
            else:
                consistency = f"Most Often {largest}"

        identity = identity_map.get(endpoint, {})
        list_of_endpoints = identity.get("list_of_ips")
        list_of_names = identity.get("list_of_names")

        endpoint_records = []

        def _calc_when(ts):
            delta = datetime.datetime.now() - ts
            overall_mins = delta.days * 24 * 60 + (delta.seconds) / 60
            whenData = pd.DataFrame({"in_minutes": [overall_mins]})
            whenData["when"] = pd.cut(
                whenData["in_minutes"], bins=bins, labels=labels, right=False
            )
            when = whenData.to_dict().get("when")
            return when.get(0)

        for result in records["discos"]:
            ep_record = {"endpoint": endpoint}
            hostname = tools.getr(result, "DeviceInfo.hostname", None)
            if not hostname and list_of_names:
                # Fall back to the first identity name when hostname is absent
                hostname = list_of_names[0]
            os_type = tools.getr(result, "DeviceInfo.os_type", None)
            os_class = tools.getr(result, "DeviceInfo.os_class", None)
            disco_run = tools.getr(result, "DiscoveryRun.label", None)
            run_start = tools.getr(result, "DiscoveryRun.starttime", None)
            run_end = tools.getr(result, "DiscoveryRun.endtime", None)
            scan_start = tools.getr(result, "DiscoveryAccess.scan_starttime", None)
            scan_end = tools.getr(result, "DiscoveryAccess.scan_endtime")
            scan_end_raw = tools.getr(result, "DiscoveryAccess.scan_endtime_raw", None)
            ep_timestamp = None
            if scan_end_raw:
                try:
                    ep_timestamp = datetime.datetime.fromisoformat(
                        scan_end_raw.replace("Z", "+00:00")
                    )
                except ValueError:
                    logger.debug(
                        "Failed to parse Scan_Endtime_Raw %r", scan_end_raw
                    )
            if ep_timestamp is None and scan_end:
                scan_end_str = " ".join(scan_end.split(" ")[:2])
                ep_timestamp = datetime.datetime.strptime(
                    scan_end_str, "%Y-%m-%d %H:%M:%S"
                )
            time_now = datetime.datetime.now(ep_timestamp.tzinfo) if ep_timestamp else datetime.datetime.now()
            delta = time_now - ep_timestamp if ep_timestamp else datetime.timedelta()
            overall_mins = delta.days * 24 * 60 + (delta.seconds) / 60
            whenData = pd.DataFrame({"in_minutes": [overall_mins]})
            whenData["when"] = pd.cut(
                whenData["in_minutes"], bins=bins, labels=labels, right=False
            )
            when = whenData.to_dict().get("when")
            whenWasThat = when.get(0)
            current_access = tools.getr(result, "DiscoveryAccess.current_access", None)
            os_version = tools.getr(result, "DeviceInfo.os_version", None)
            node_updated = tools.getr(result, "DiscoveryAccess.host_node_updated", None)
            end_state = tools.getr(result, "DiscoveryAccess.end_state", None)
            prev_end_state = tools.getr(result, "DiscoveryAccess.previous_end_state", None)
            reason_not_updated = tools.getr(result, "DiscoveryAccess.reason_not_updated", None)
            session_results_logged = tools.getr(
                result, "DiscoveryAccess.session_results_logged", None
            )
            node_kind = result.get("DeviceInfo.kind") or result.get("DeviceInfo.inferred_kind")
            if isinstance(node_kind, list):
                node_kind = tools.sortlist(node_kind)
            last_credential = tools.getr(result, "DeviceInfo.last_credential", None)
            credential_name = None
            credential_login = None
            if last_credential:
                cred_det = tools.get_credential(vaultcreds, last_credential)
                credential_name = tools.getr(cred_det, "label", "Not Found")
                credential_login = tools.getr(cred_det, "username", "Not Found")
            node_id = result.get("DiscoveryAccess.id")
            prev_node_id = result.get("DiscoveryAccess.previous_id")
            next_node_id = result.get("DiscoveryAccess.next_id")
            last_marker = result.get("DiscoveryAccess._last_marker")

            ep_record.update(
                {
                    "hostname": hostname,
                    "list_of_names": list_of_names,
                    "list_of_endpoints": list_of_endpoints,
                    "node_kind": node_kind,
                    "os_type": os_type,
                    "os_version": os_version,
                    "os_class": os_class,
                    "disco_run": disco_run,
                    "run_start": run_start,
                    "run_end": run_end,
                    "scan_start": scan_start,
                    "scan_end": scan_end,
                    "scan_end_raw": scan_end_raw,
                    "when_was_that": whenWasThat,
                    "consistency": consistency,
                    "current_access": current_access,
                    "node_updated": node_updated,
                    "reason_not_updated": reason_not_updated,
                    "end_state": end_state,
                    "previous_end_state": prev_end_state,
                    "session_results_logged": session_results_logged,
                    "last_credential": last_credential,
                    "credential_name": credential_name,
                    "credential_login": credential_login,
                    "timestamp": ep_timestamp,
                    "da_id": node_id,
                    "prev_da_id": prev_node_id,
                    "next_node_id": next_node_id,
                    "last_marker": last_marker,
                }
            )
            endpoint_records.append(ep_record)

        for result in records["dropped"]:
            run_end = tools.getr(result, "End")
            scan_end_raw = tools.getr(result, "End_Raw", None)
            hostname = list_of_names[0] if list_of_names else None
            ep_timestamp = None
            if scan_end_raw:
                try:
                    ep_timestamp = datetime.datetime.fromisoformat(
                        scan_end_raw.replace("Z", "+00:00")
                    )
                except ValueError:
                    logger.debug("Failed to parse End_Raw %r", scan_end_raw)
            if ep_timestamp is None and run_end:
                run_end_str = " ".join(run_end.split(" ")[:2])
                ep_timestamp = datetime.datetime.strptime(
                    run_end_str, "%Y-%m-%d %H:%M:%S"
                )
            time_now = datetime.datetime.now(ep_timestamp.tzinfo) if ep_timestamp else datetime.datetime.now()
            delta = time_now - ep_timestamp if ep_timestamp else datetime.timedelta()
            overall_mins = delta.days * 24 * 60 + (delta.seconds) / 60
            whenData = pd.DataFrame({"in_minutes": [overall_mins]})
            whenData["when"] = pd.cut(
                whenData["in_minutes"], bins=bins, labels=labels, right=False
            )
            when = whenData.to_dict().get("when")
            whenWasThat = when.get(0)
            disco_run = tools.getr(result, "Run", None)
            run_start = tools.getr(result, "Start", None)
            end_state = tools.getr(result, "End_State", None)
            reason_not_updated = tools.getr(result, "Reason_Not_Updated", None)
            run_end_timestamp = ep_timestamp
            ep_record = {
                "endpoint": endpoint,
                "hostname": hostname,
                "list_of_names": list_of_names,
                "list_of_endpoints": list_of_endpoints,
                "disco_run": disco_run,
                "run_start": run_start,
                "run_end": run_end,
                "when_was_that": whenWasThat,
                "consistency": consistency,
                "reason_not_updated": reason_not_updated,
                "end_state": end_state,
                "timestamp": run_end_timestamp,
                "scan_end_raw": scan_end_raw,
            }
            endpoint_records.append(ep_record)

        if not endpoint_records:
            continue

        named_records = [
            r for r in endpoint_records if r.get("hostname") or r.get("credential_name")
        ]
        latest = max(endpoint_records, key=lambda r: r["timestamp"])
        if named_records:
            chosen = max(named_records, key=lambda r: r["timestamp"])
        else:
            chosen = latest
        chosen["timestamp"] = latest.get("timestamp")
        chosen["when_was_that"] = latest.get("when_was_that")
        if latest.get("scan_end_raw"):
            chosen["scan_end_raw"] = latest.get("scan_end_raw")

        # Merge selected fields from the latest record when missing in the chosen
        # record. This ensures the most recent information (such as node update
        # times or credential details) is available even if the "best" record is
        # older because it contains identifying information like hostname.
        merge_fields = [
            "hostname",
            "node_updated",
            "credential_name",
            "credential_login",
            "last_credential",
            "current_access",
            "end_state",
            "previous_end_state",
            "reason_not_updated",
            "consistency",
            "session_results_logged",
            "da_id",
            "prev_da_id",
            "next_node_id",
            "last_marker",
        ]

        for field in merge_fields:
            if chosen.get(field) in (None, "") and latest.get(field) not in (None, ""):
                chosen[field] = latest.get(field)
        # Sort so the newest record is first; older records follow
        sorted_records = sorted(
            endpoint_records,
            key=lambda r: r.get("timestamp") or datetime.datetime.min,
            reverse=True,
        )

        # Start with the most recent record and fill in any missing details
        merged_record = sorted_records[0].copy()
        timestamp_fields = {"timestamp", "when_was_that", "scan_end_raw"}

        for record in sorted_records[1:]:
            for key, value in record.items():
                if key in timestamp_fields:
                    # Preserve timestamp-related fields from the latest record
                    continue
                if merged_record.get(key) in (None, "") and value not in (None, ""):
                    # Fill missing data from older records without overwriting
                    # existing non-empty values with None
                    merged_record[key] = value

        disco_data.append(merged_record)

    return disco_data


@output._timer("Outpost Credentials")
def outpost_creds(creds_ep, search_ep, appliance, args):
    """Report mapping of outpost credentials to their outposts."""

    outpost_map = api.get_outpost_credential_map(search_ep, appliance) or {}

    vault = api.get_json(creds_ep.get_vault_credentials)
    label_map = {
        c.get("uuid"): c.get("label")
        for c in (vault or [])
        if isinstance(c, dict)
    }

    rows = []
    for op_id, info in outpost_map.items():
        url = info.get("url")
        for uuid in info.get("credentials", []):
            rows.append([url, op_id, uuid, label_map.get(uuid)])

    output.report(
        rows,
        ["Outpost", "Outpost Id", "Credential UUID", "Credential Label"],
        args,
        name="outpost_creds",
    )


@output._timer("Discovery Access")
def discovery_access(twsearch, twcreds, args):
    """Generate basic discovery access report."""
    logger.info("Running Discovery Access Report")
    disco_data = _gather_discovery_data(twsearch, twcreds, args)

    if disco_data:
        headers = list(dict.fromkeys(disco_data[0].keys()))
        rows = [[record.get(h) for h in headers] for record in disco_data]
    else:
        headers, rows = [], []

    output.report(rows, headers, args, name="discovery_access")
    return disco_data


@output._timer("Discovery Access Analysis")
def discovery_analysis(twsearch, twcreds, args, disco_data=None):
    print("\nDiscovery Access Analysis")
    print("-------------------------")
    logger.info("Running DA Analysis Report")
    print("Running DA Analysis Report")

    # Reuse provided discovery data if available; otherwise gather it
    # independently so the function can be executed stand-alone.
    if disco_data is None:
        disco_data = _gather_discovery_data(twsearch, twcreds, args)

    for record in disco_data:
        current = record.get("end_state")
        previous = record.get("previous_end_state")
        dropped = record.get("dropped", 0)
        if previous is None:
            if dropped > 1 and current in ["DarkSpace", "AlreadyProcessing", "Excluded"]:
                previous = current
            else:
                previous = "First Scan"
        record["change"] = f"{previous} -> {current}"

    msg = os.linesep
    data = []
    headers = []

    for ddata in disco_data:
        # Use the same approach as the devices report: fall back to the first
        # known device name from the identity when a hostname is unavailable.
        device_name = ddata.get("hostname")
        if not device_name:
            names = ddata.get("list_of_names") or []
            if isinstance(names, list) and names:
                device_name = names[0]

        node_updated = ddata.get("node_updated")
        cred_name = ddata.get("credential_name")

        if args.output_csv or args.output_file:
            data.append([
                ddata.get("endpoint"),
                device_name,
                ddata.get("list_of_names"),
                ddata.get("list_of_endpoints"),
                ddata.get("node_kind"),
                ddata.get("os_type"),
                ddata.get("os_version"),
                ddata.get("os_class"),
                ddata.get("disco_run"),
                ddata.get("run_start"),
                ddata.get("run_end"),
                ddata.get("scan_start"),
                ddata.get("scan_end"),
                ddata.get("scan_end_raw"),
                ddata.get("when_was_that"),
                ddata.get("consistency"),
                ddata.get("current_access"),
                ddata.get("access_method"),
                node_updated,
                ddata.get("reason_not_updated"),
                ddata.get("end_state"),
                ddata.get("previous_end_state"),
                ddata.get("change"),
                ddata.get("session_results_logged"),
                ddata.get("last_credential"),
                cred_name,
                ddata.get("credential_login"),
                ddata.get("timestamp"),
                ddata.get("da_id"),
                ddata.get("prev_da_id"),
                ddata.get("next_node_id"),
                ddata.get("dropped"),
            ])
            headers = [
                "endpoint",
                "device_name",
                "list_of_device_names",
                "list_of_endpoints",
                "node_kind",
                "os_type",
                "os_version",
                "os_class",
                "discovery_run",
                "discovery_run_start",
                "discovery_run_end",
                "scan_start",
                "scan_end",
                "scan_end_raw",
                "when_was_that",
                "consistency",
                "current_access",
                "access_method",
                "inferred_node_updated",
                "reason_not_updated",
                "end_state",
                "previous_end_state",
                "end_state_change",
                "session_results_logged",
                "last_credential",
                "credential_name",
                "credential_login",
                "timestamp",
                "da_id",
                "prev_da_id",
                "next_node_id",
                "dropped",
            ]
        else:
            msg = (
                "\nOnly showing limited details for table output. Output to CSV for full results.\n"
            )
            data.append([
                ddata.get("endpoint"),
                device_name,
                ddata.get("when_was_that"),
                node_updated,
                ddata.get("consistency"),
                ddata.get("change"),
                cred_name,
            ])
            headers = [
                "endpoint",
                "device_name",
                "when_was_that",
                "inferred_node_updated",
                "consistency",
                "end_state_change",
                "credential_name",
            ]

    print(msg)

    try:
        data.sort(
            key=lambda k: (
                isinstance(tools.ip_or_string(k[0]), str),
                tools.ip_or_string(k[0]),
            )
        )
    except TypeError as e:
        msg = "TypeError: Data output can't be hashed (cannot be sorted)\nError: %s" % str(e)
        print(msg)
        logger.error(msg)

    output.report(data, headers, args, name="discovery_analysis")


@output._timer("Discovery Run Analysis")
def discovery_run_analysis(twsearch, twcreds, args):
    """Report on discovery run ranges and endpoint statistics."""
    logger.info("Running Discovery Run Analysis report")
    results = api.search_results(twsearch, queries.discovery_run_analysis)

    if isinstance(results, list) and results:
        headers = list(results[0].keys())
        rows = [[record.get(h) for h in headers] for record in results]
    else:
        headers, rows = [], []

    output.report(rows, headers, args, name="discovery_run_analysis")


@output._timer("TPL Export")
def tpl_export(search, query, dir, method, client, sysuser, syspass):
    tpldir = dir + "/tpl"
    if not os.path.exists(tpldir):
        os.makedirs(tpldir)
    files=0
    if method == "api":
        response = api.search_results(search, query)
        if type(response) == list and len(response) > 0:
            header, data, header_hf = tools.json2csv(response)
            for row in data:
                filename = "%s/%s.tpl"%(tpldir,row[1])
                files+=1
                try:
                    f=open(filename, 'w', encoding="utf-8")
                    f.write(row[0])
                    f.close()
                except Exception as e:
                    logger.error("Problem with TPL: %s\n%s\n%s\nRow Data:\n%s"%(filename,e.__class__,str(e),row))
                    output.txt_dump(str(row),"%s/module_%s.tpl"%(tpldir,files))
        else:
            output.txt_dump("No results.","%s/tpl_export.txt"%tpldir)
    else:
        results = cli.run_query(client,sysuser,syspass,query)
        try:
            body = results.split("\n",1)[1]
            for line in body.split("\r\n"):
                files+=1
                if line:
                    try:
                        columns = [c.strip() for c in line.split(',')]
                        filename = "%s/%s.tpl"%(tpldir,columns[0])
                        columns.pop(0)
                        row = [ tools.dequote(columns) ]
                        logger.debug("Parsing row: %s", row)
                        row2 = ''.join(row[0])
                        row3 = tools.dequote(row2)
                        newrow = row3.replace('""""','","')
                        logger.debug("NEW row: %s", newrow)
                        try:
                            f=open(filename, 'w', encoding="utf-8")
                            f.write(newrow)
                            f.close()
                        except Exception as e:
                            logger.error("Problem with TPL: %s\n%s\n%s\nRow Data:\n%s"%(filename,e.__class__,str(e),row))
                            output.txt_dump(str(row),"%s/module_%s.tpl"%(tpldir,files))
                    except Exception as e:
                        logger.error("Problem with TPL:\n%s\n%s\nRow Data:\n%s"%(e.__class__,str(e),line))
                        # Dump
                        output.txt_dump(str(line),"%s/module_%s.tpl"%(tpldir,files))
        except Exception as e:
            logger.error("Problem parsing data:\n%s\n%s"%(e.__class__,str(e)))
            # Try dumping it instead
            output.txt_dump(results,"%s/tpl_export.txt"%tpldir)
