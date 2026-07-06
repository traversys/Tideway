# Discovery API commands for DisMAL

import sys
import logging
import csv
import json
import os
import time
import io
from urllib.parse import urlparse

# PIP Modules
from pprint import pprint
import pandas
import tideway

# Local
from . import (
    tools,
    output,
    builder,
    queries,
    defaults,
    reporting,
    access,
    common_agents,
    cache,
)
import socket

logger = logging.getLogger("_api_")

# Cache for search_results to avoid duplicate API calls
_SEARCH_CACHE = {}
_CACHE_ENDPOINT = None


class APITimeoutError(RuntimeError):
    """Raised when the Discovery API repeatedly times out."""

    pass

def init_endpoints(api_target, args):
    try:
        logger.debug("Requesting discovery endpoint from %s", args.target)
        disco = api_target.discovery()
        logger.debug("Discovery endpoint obtained: %s", disco)
    except:
        msg = "Error getting Discovery endpoint from %s\n" % (args.target)
        print(msg)
        logger.error(msg)
        sys.exit(1)
    try:
        logger.debug("Requesting data endpoint from %s", args.target)
        search = api_target.data()
        logger.debug("Data endpoint obtained: %s", search)
    except:
        msg = "Error getting Data endpoint from %s\n" % (args.target)
        print(msg)
        logger.error(msg)
        sys.exit(1)
    try:
        logger.debug("Requesting credentials endpoint from %s", args.target)
        creds = api_target.credentials()
        logger.debug("Credentials endpoint obtained: %s", creds)
    except:
        msg = "Error getting Credentials endpoint from %s\n" % (args.target)
        print(msg)
        logger.error(msg)
        sys.exit(1)
    try:
        logger.debug("Requesting vault endpoint from %s", args.target)
        vault = api_target.vault()
        logger.debug("Vault endpoint obtained: %s", vault)
    except:
        msg = "Error getting Vault endpoint from %s\n" % (args.target)
        print(msg)
        logger.error(msg)
        sys.exit(1)
    try:
        logger.debug("Requesting knowledge endpoint from %s", args.target)
        knowledge = api_target.knowledge()
        logger.debug("Knowledge endpoint obtained: %s", knowledge)
    except:
        msg = "Error getting Knowledge endpoint from %s\n" % (args.target)
        print(msg)
        logger.error(msg)
        sys.exit(1)
    return disco, search, creds, vault, knowledge

def get_json(api_endpoint):
    """Return JSON data from a request object.

    The ``tideway`` library lazily performs the HTTP request when an attribute
    such as ``status_code`` is accessed.  Because of this we must be prepared
    for network related exceptions to be raised here.  Any errors result in an
    empty dictionary being returned so callers can handle the failure
    gracefully.
    """

    # If the endpoint is callable (for example a property), call it first
    if callable(api_endpoint):
        try:
            api_endpoint = api_endpoint()
        except Exception as e:  # pragma: no cover - network errors
            if logger.isEnabledFor(logging.DEBUG):
                msg = (
                    "Not able to make api call.\nException: %s\n%s"
                    % (e.__class__, str(e))
                )
                print(msg)
                logger.error(msg)
            else:
                msg = (
                    "Not able to make api call. Rerun in debug mode for more "
                    "information."
                )
                print(msg)
                logger.error("Not able to make api call", exc_info=e)
            return {}

    if not hasattr(api_endpoint, "status_code"):
        if isinstance(api_endpoint, (list, dict)):
            return api_endpoint
        logger.error("Invalid API endpoint provided to get_json")
        return {}

    status_code = api_endpoint.status_code
    url = getattr(api_endpoint, "url", "unknown")

    if status_code == 200:
        msg = "Called API endpoint: %s\nStatus: %s - %s\n" % (
            url,
            status_code,
            api_endpoint.ok,
        )
        logger.info(msg)
    else:
        msg = "Failed to get API endpoint: %s\nReason: %s - %s\n" % (
            url,
            status_code,
            api_endpoint.reason,
        )
        if status_code == 404:
            logger.warning(msg)
        else:
            print(msg)
            logger.error(msg)

    if logger.isEnabledFor(logging.DEBUG):
        try:
            logger.debug("API response text from %s:\n%s", url, api_endpoint.text)
        except Exception:
            pass

    try:
        data = api_endpoint.json()
    except Exception as e:  # pragma: no cover - unexpected JSON issues
        msg = "Error decoding JSON from %s: %s" % (url, str(e))
        print(msg)
        logger.error(msg)
        return {}
    else:
        if logger.isEnabledFor(logging.DEBUG):
            try:
                logger.debug("Decoded JSON from %s:\n%s", url, json.dumps(data, indent=2))
            except Exception:
                pass
        return data

def admin(disco,args,dir):
    logger.debug("Calling disco.admin() with no parameters")
    data = disco.admin()
    logger.debug(
        "disco.admin() response ok=%s status=%s text=%s",
        getattr(data, "ok", "N/A"),
        getattr(data, "status_code", "N/A"),
        getattr(data, "text", "N/A"),
    )
    result = get_json(data)
    os_version = result['versions']['os_updates']
    logger.info('OS Version:\n%s'%os_version)
    logger.info('Discovery Version:\n%s'%os_version)
    output.define_txt(args,json.dumps(result['versions']),os.path.join(dir, defaults.api_filename),None)

def audit(search,args,dir):
    output.define_csv(args,search,queries.audit,os.path.join(dir, defaults.audit_filename),args.output_file,args.target,"query")

def baseline(disco, args, dir):
    logger.debug("Calling disco.baseline() with no parameters")
    data = disco.baseline()
    logger.debug(
        "disco.baseline() response ok=%s status=%s text=%s",
        getattr(data, "ok", "N/A"),
        getattr(data, "status_code", "N/A"),
        getattr(data, "text", "N/A"),
    )
    logger.info("Checking Baseline...")
    bl = get_json(data)
    if bl:
        baseline = json.loads(json.dumps(bl))
        logger.debug('Baseline Status:\n%s'%bl)
        # Last Message
        try:
            if 'summary' in baseline:
                # Helix does not share the baseline
                last_message = baseline['summary']['last_message']
                # Failures
                header = []
                rows = []
                if "FAILED" in baseline['results']:
                    failures = baseline['results']['FAILED']
                    header, rows, _ = tools.json2csv(failures)
                header.insert(0, "Discovery Instance")
                for row in rows:
                    row.insert(0, args.target)
                output.define_csv(
                    args,
                    header,
                    rows,
                    os.path.join(dir, defaults.baseline_filename),
                    args.output_file,
                    args.target,
                    "csv_file",
                )
        except Exception as e:
            logger.error("Problem with baseline:\n%s\n%s"%(e.__class__,str(e)))
            # Try dumping it
            output.txt_dump(bl,dir+"/baseline_status.txt")
    else:
        last_message = bl
        output.txt_dump(last_message,dir+"/baseline_status.txt")

def cmdb_config(search, args, dir):
    output.define_csv(args,search,queries.cmdb_sync_config,os.path.join(dir, defaults.cmdbsync_filename),args.output_file,args.target,"query")

def modules(search, args, dir):
    output.define_csv(args,search,queries.patterns,os.path.join(dir, defaults.tw_knowledge_filename),args.output_file,args.target,"query")

def licensing(disco, args, dir):
    try:
        # CSV
        logger.debug("Calling disco.licensing(content_type='csv')")
        r = disco.licensing(content_type="csv")
        logger.debug(
            "disco.licensing() response ok=%s status=%s text=%s",
            getattr(r, "ok", "N/A"),
            getattr(r, "status_code", "N/A"),
            getattr(r, "text", "N/A"),
        )
        handle = open(os.path.join(dir, defaults.tw_license_zip_filename), "wb")
        for chunk in r.iter_content(chunk_size=512):
            if chunk:  # filter out keep-alive new chunks
                handle.write(chunk)
    except:
        # Plaintext
        logger.debug("Calling disco.licensing() with no parameters")
        r = disco.licensing()
        logger.debug(
            "disco.licensing() response ok=%s status=%s text=%s",
            getattr(r, "ok", "N/A"),
            getattr(r, "status_code", "N/A"),
            getattr(r, "text", "N/A"),
        )
        handle = open(os.path.join(dir, defaults.tw_license_raw_filename), "wb")
        for chunk in r.iter_content(chunk_size=512):
            if chunk:  # filter out keep-alive new chunks
                handle.write(chunk)

def query(search, args):
    """Run an ad-hoc query against the search endpoint."""
    results = []
    try:
        if hasattr(search, "search_bulk"):
            results = search.search_bulk(args.a_query, limit=500)
        else:
            results = search.search(args.a_query, format="object", limit=500)
    except Exception as e:
        if logger.isEnabledFor(logging.DEBUG):
            msg = (
                "Not able to make api call.\nQuery: %s\nException: %s\n%s"
                % (args.a_query, e.__class__, str(e))
            )
            print(msg)
            logger.error(msg)
        else:
            msg = "Not able to make api call. Rerun in debug mode for more information."
            print(msg)
            logger.error(
                "Not able to make api call for query %s", args.a_query, exc_info=e
            )
    if len(results) > 0:
        if args.output_csv:
            w = csv.writer(sys.stdout)
            w.writerows(results)
        elif args.output_file:
            with open(args.output_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(results)
                msg = "Report saved to %s" % args.output_file
                print(msg)
                logger.info(msg)
        else:
            pprint(results)
    else:
        msg = "No results found!\n"
        print(msg)
        logger.warning(msg)

def get_outposts(appliance):
    """Return list of Discovery Outposts from the appliance."""
    logger.debug("Calling appliance.get('/discovery/outposts?deleted=false')")
    resp = appliance.get("/discovery/outposts?deleted=false")
    logger.debug(
        "outposts response ok=%s status=%s text=%s",
        getattr(resp, "ok", "N/A"),
        getattr(resp, "status_code", "N/A"),
        getattr(resp, "text", "N/A"),
    )
    return get_json(resp)


def map_outpost_credentials(appliance, include_details=False):
    """Return mapping of credential UUIDs to outpost URLs.

    If ``include_details`` is ``True`` a tuple ``(mapping, credentials)`` is
    returned where ``credentials`` is a list of credential dictionaries
    retrieved from the outposts.  When ``False`` only the mapping is returned
    to maintain backwards compatibility.
    """
    mapping = {}
    credentials = []
    outposts = get_outposts(appliance)
    if not isinstance(outposts, list):
        return (mapping, credentials) if include_details else mapping
    token = getattr(appliance, "token", None)
    api_version = getattr(appliance, "api_version", None)
    for outpost in outposts:
        url = outpost.get("url")
        if not url:
            continue
        parsed = urlparse(url)
        host = parsed.hostname or (parsed.netloc or parsed.path).split(":")[0]
        if access.ping(host) != 0:
            msg = f"Outpost {url} is not available"
            print(msg)
            logger.warning(msg)
            continue
        target = (parsed.netloc or parsed.path).rstrip("/")
        try:
            op_app = tideway.outpost(target, token, api_version=api_version)
            creds_ep = op_app.credentials()
            cred_list = get_json(creds_ep.get_vault_credentials)
            for cred in cred_list or []:
                uuid = cred.get("uuid")
                if not uuid:
                    continue
                detail = get_json(creds_ep.get_vault_credential(uuid))
                mapping[uuid] = url
                if include_details and isinstance(detail, dict):
                    credentials.append(detail)
        except Exception as e:  # pragma: no cover - network errors
            logger.error("Error processing outpost %s: %s", url, e)
    return (mapping, credentials) if include_details else mapping


def get_outpost_credential_map(search, appliance):
    """Return mapping of outpost IDs to credential information.

    The mapping is built using a search query to associate credential UUIDs
    with outpost identifiers and a single call to :func:`get_outposts` to
    resolve those identifiers to URLs.  The returned structure is a
    dictionary in the form::

        {
            "<outpost_id>": {
                "url": "http://outpost",
                "credentials": ["<uuid>", ...],
            },
            ...
        }

    Previously this function returned a mapping of credential UUIDs to
    outpost URLs which did not provide a reverse lookup for credentials and
    caused ``reporting.outpost_creds`` to fail when iterating over the
    mapping.  The new structure groups credentials by outpost and exposes
    the outpost URL alongside the list of credential UUIDs.
    """

    mapping = {}

    results = search_results(search, queries.outpost_credentials)
    if isinstance(results, dict):
        results = results.get("results", [])
    if not isinstance(results, list):
        results = []

    cred_to_outpost = {}
    for entry in results:
        if not isinstance(entry, dict):
            continue
        uuid = entry.get("credential")
        outpost_id = entry.get("outpost")
        if uuid and outpost_id:
            cred_to_outpost[str(uuid)] = str(outpost_id)

    if not cred_to_outpost:
        return mapping

    outposts = get_outposts(appliance)
    id_to_url = {}
    if isinstance(outposts, list):
        for op in outposts:
            if not isinstance(op, dict):
                continue
            op_id = (
                op.get("id")
                or op.get("outpost")
                or op.get("outpost_id")
                or op.get("uuid")
            )
            url = op.get("url")
            if op_id and url:
                id_to_url[str(op_id)] = url

    for uuid, op_id in cred_to_outpost.items():
        url = id_to_url.get(str(op_id))
        if not url:
            continue
        op_entry = mapping.setdefault(op_id, {"url": url, "credentials": []})
        op_entry["credentials"].append(uuid)

    return mapping

def success(twcreds, twsearch, args, dir):
    reporting.successful(twcreds, twsearch, args)
    #if args.output_file:
    #    df = pandas.read_csv(args.output_file)
    #    df.insert(0, "Discovery Instance", args.target)
    #    df.to_csv(os.path.join(dir, defaults.success_filename), index=False)
    #    os.remove(args.output_file)

def schedules(search, args, dir):
    output.define_csv(args,search,queries.scan_ranges,os.path.join(dir, defaults.scan_ranges_filename),args.output_file,args.target,"query")

def excludes(search, args, dir):
    output.define_csv(args,search,queries.exclude_ranges,os.path.join(dir, defaults.exclude_ranges_filename),args.output_file,args.target,"query")

def discovery_runs(disco, args, dir):
    logger.info("Checking Scan ranges...")
    logger.debug("Calling disco.get_discovery_runs")
    api_response = disco.get_discovery_runs
    logger.debug(
        "disco.get_discovery_runs response ok=%s status=%s text=%s",
        getattr(api_response, "ok", "N/A"),
        getattr(api_response, "status_code", "N/A"),
        getattr(api_response, "text", "N/A"),
    )
    r = get_json(api_response)
    if r:
        runs = json.loads(json.dumps(r))
        logger.debug('Runs:\n%s' % r)
        header, rows, _ = tools.json2csv(runs)
        header.insert(0, "Discovery Instance")
        int_fields = {"done", "pre_scanning", "scanning", "total"}
        for row in rows:
            row.insert(0, args.target)
            for idx, field in enumerate(header[1:], start=1):
                if field.split(".")[-1] in int_fields:
                    try:
                        row[idx] = int(row[idx])
                    except (ValueError, TypeError):
                        pass
        output.define_csv(
            args,
            header,
            rows,
            os.path.join(dir, defaults.active_scans_filename),
            args.output_file,
            args.target,
            "csv_file",
        )

def show_runs(disco, args):
    logger.debug("Calling disco.get_discovery_runs")
    api_response = disco.get_discovery_runs
    logger.debug(
        "disco.get_discovery_runs response ok=%s status=%s text=%s",
        getattr(api_response, "ok", "N/A"),
        getattr(api_response, "status_code", "N/A"),
        getattr(api_response, "text", "N/A"),
    )
    runs = get_json(api_response)
    if not runs:
        msg = "No runs in progress."
        print(msg)
        logger.error(msg)
        return
    parsed_runs = []
    headers = []
    for run in runs:
        disco_run = {}
        for key in run:
            disco_run.update({key: run[key]})
            headers.append(key)
        parsed_runs.append(disco_run)

    headers = tools.sortlist(headers)
    run_csvs = []
    for run in parsed_runs:
        run_csv = []
        for header in headers:
            value = run.get(header)
            run_csv.append(value)
        run_csvs.append(run_csv)

    export = getattr(args, "export", False)
    outfile = getattr(args, "file", getattr(args, "output_file", None))
    if export:
        w = csv.writer(sys.stdout)
        w.writerow(raw_headers)
        w.writerows(run_csvs)
    elif outfile:
        with open(outfile, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(raw_headers)
            writer.writerows(run_csvs)
            msg = "Report saved to %s" % outfile
            print(msg)
            logger.info(msg)
    else:
        if getattr(args, "excavate", None):
            out_dir = getattr(args, "reporting_dir", "")
            path = os.path.join(out_dir, defaults.active_scans_filename)
            output.define_csv(
                args,
                headers,
                run_csvs,
                path,
                getattr(args, "output_file", None),
                getattr(args, "target", None),
                "csv_file",
            )
        elif getattr(args, "debugging", False):
            pprint(runs)
        else:
            print(f"Active discovery runs: {len(runs)}")
            for r in runs:
                rid = r.get("run_id") or r.get("id") or r.get("label") or "N/A"
                status = r.get("status", "unknown")
                print(f" - {rid}: {status}")

def sensitive(search, args, dir):
    try:
        results = search_results(search, queries.sensitive_data)
    except APITimeoutError as e:
        msg = (
            "Sensitive data query timed out (504) after multiple retries. "
            "Continuing without this report."
        )
        print(msg)
        logger.warning(msg)
        results = []
    count = len(results) if isinstance(results, list) else 0
    tools.completage("Processing", count or 1, (count or 1) - 1)
    print(os.linesep, end="\r")
    header, rows = [], []
    if isinstance(results, list) and results:
        header, rows, _ = tools.json2csv(results)
        header.insert(0, "Discovery Instance")
        for row in rows:
            row.insert(0, args.target)
    else:
        header.insert(0, "Discovery Instance")
    output.define_csv(
        args,
        header,
        rows,
        os.path.join(dir, defaults.sensitive_data_filename),
        args.output_file,
        args.target,
        "csv_file",
    )


def outpost_creds(creds, search, args, dir):
    """Wrapper for the outpost credential report."""
    # Some endpoints do not expose an `appliance` attribute; use the endpoint
    # itself when it provides the `get` method.
    appliance = getattr(creds, "appliance", None) or (creds if hasattr(creds, "get") else None)
    reporting.outpost_creds(creds, search, appliance, args)

def tpl_export(search, args, dir):
    reporting.tpl_export(search, queries.tpl_export, dir, "api", None, None, None)

@output._timer("ECA Errors")
def eca_errors(search, args, dir):
    results = search_results(search, queries.eca_error)
    count = len(results) if isinstance(results, list) else 0
    tools.completage("Processing", count or 1, (count or 1) - 1)
    print(os.linesep, end="\r")
    header, rows = [], []
    if isinstance(results, list) and results:
        header, rows, _ = tools.json2csv(results)
        header.insert(0, "Discovery Instance")
        for row in rows:
            row.insert(0, args.target)
    else:
        header.insert(0, "Discovery Instance")
    output.define_csv(
        args,
        header,
        rows,
        os.path.join(dir, defaults.eca_errors_filename),
        args.output_file,
        args.target,
        "csv_file",
    )

@output._timer("Open Ports")
def open_ports(search, args, dir):
    results = search_results(search, queries.open_ports)
    count = len(results) if isinstance(results, list) else 0
    tools.completage("Processing", count or 1, (count or 1) - 1)
    print(os.linesep, end="\r")
    header, rows = [], []
    if isinstance(results, list) and results:
        header, rows, _ = tools.json2csv(results)
        header.insert(0, "Discovery Instance")
        for row in rows:
            row.insert(0, args.target)
    else:
        header.insert(0, "Discovery Instance")
    output.define_csv(
        args,
        header,
        rows,
        os.path.join(dir, defaults.open_ports_filename),
        args.output_file,
        args.target,
        "csv_file",
    )

def device_capture_candidates(search, args, dir):
    """Export capture candidates, defaulting missing sysobjectid to 0."""
    results = search_results(search, queries.capture_candidates)
    header, rows, _ = tools.json2csv(results or [])
    if "DeviceInfo.sysobjectid" in header:
        idx = header.index("DeviceInfo.sysobjectid")
        for row in rows:
            if row[idx] is None:
                row[idx] = 0
    header.insert(0, "Discovery Instance")
    for row in rows:
        row.insert(0, args.target)
    output.define_csv(
        args,
        header,
        rows,
        os.path.join(dir, defaults.capture_candidates_filename),
        args.output_file,
        args.target,
        "csv_file",
    )

@output._timer("Host Utilisation")
def host_util(search, args, dir):
    results = search_results(search, queries.host_utilisation)
    count = len(results) if isinstance(results, list) else 0
    tools.completage("Processing", count or 1, (count or 1) - 1)
    print(os.linesep, end="\r")
    header, rows = [], []
    if isinstance(results, list) and results:
        header, rows, _ = tools.json2csv(results, return_map=True)
        header.insert(0, "Discovery Instance")
        numeric_cols = {
            "Host.running_software_instances",
            "Host.candidate_software_instances",
            "Host.running_processes",
            "Host.running_services",
        }
        for row in rows:
            row.insert(0, args.target)
            for idx, field in enumerate(header[1:], start=1):
                if field in numeric_cols:
                    try:
                        row[idx] = int(row[idx])
                    except (ValueError, TypeError):
                        row[idx] = 0
    else:
        header = ["Discovery Instance"]
    output.define_csv(
        args,
        header,
        rows,
        os.path.join(dir, defaults.host_util_filename),
        args.output_file,
        args.target,
        "csv_file",
    )

@output._timer("Orphan VMs")
def orphan_vms(search, args, dir):
    results = search_results(search, queries.orphan_vms)
    if not isinstance(results, list) or not all(isinstance(r, dict) for r in results):
        logger.error(
            "Unexpected search results type for orphan_vms: %s",
            type(results).__name__,
        )
        output.csv_file([], [], os.path.join(dir, defaults.orphan_vms_filename))
        return

    headers = []
    rows = []
    for r in results or []:
        if not headers:
            headers = list(r.keys())
        rows.append([r.get(h) for h in headers])
    headers.insert(0, "Discovery Instance")
    for row in rows:
        row.insert(0, args.target)
    output.csv_file(rows, headers, os.path.join(dir, defaults.orphan_vms_filename))

@output._timer("Missing VMs")
def missing_vms(search, args, dir):
    if getattr(args, "resolve_hostnames", False):
        response = search_results(search, queries.missing_vms)
        if isinstance(response, list) and len(response) > 0:
            header, data, _ = tools.json2csv(response)
            header.insert(0, "Discovery Instance")
            for row in data:
                row.insert(0, args.target)

            gf_index = (
                header.index("VirtualMachine.guest_full_name")
                if "VirtualMachine.guest_full_name" in header
                else None
            )
            header.append("Pingable")

            devices = devices_lookup(search)

            header.extend(["last_identity", "last_scanned", "last_result"])

            timer_count = 0
            for row in data:
                timer_count = tools.completage(
                    "Resolving hostnames...",
                    len(data),
                    timer_count,
                )
                ip = "N/A"
                if gf_index is not None:
                    host = row[gf_index]
                    if host and host != "N/A" and access.ping(host) == 0:
                        try:
                            ip = socket.gethostbyname(host)
                        except Exception:
                            ip = "N/A"
                row.append(ip)
                info = devices.get(ip)
                if info:
                    row.extend([
                        info.get("last_identity", "N/A"),
                        info.get("last_start_time", "N/A"),
                        info.get("last_result", "N/A"),
                    ])
                else:
                    row.extend(["N/A", "N/A", "N/A"])
            print(os.linesep, end="\r")

            output.define_csv(
                args,
                header,
                data,
                os.path.join(dir, defaults.missing_vms_filename),
                args.output_file,
                args.target,
                "csv_file",
            )
        else:
            output.define_csv(
                args,
                search,
                queries.missing_vms,
                os.path.join(dir, defaults.missing_vms_filename),
                args.output_file,
                args.target,
                "query",
            )
    else:
        output.define_csv(
            args,
            search,
            queries.missing_vms,
            os.path.join(dir, defaults.missing_vms_filename),
            args.output_file,
            args.target,
            "query",
        )

@output._timer("Near Removal")
def near_removal(search, args, dir):
    output.define_csv(args,search,queries.near_removal,os.path.join(dir, defaults.near_removal_filename),args.output_file,args.target,"query")

@output._timer("Removed")
def removed(search, args, dir):
    output.define_csv(args,search,queries.removed,os.path.join(dir, defaults.removed_filename),args.output_file,args.target,"query")

@output._timer("OS Lifecycle")
def oslc(search, args, dir):
    output.define_csv(args,search,queries.os_lifecycle,os.path.join(dir, defaults.os_lifecycle_filename),args.output_file,args.target,"query")

@output._timer("Software Lifecycle")
def slc(search, args, dir):
    output.define_csv(args,search,queries.software_lifecycle,os.path.join(dir, defaults.si_lifecycle_filename),args.output_file,args.target,"query")

@output._timer("Database Lifecycle")
def dblc(search, args, dir):
    output.define_csv(args,search,queries.db_lifecycle,os.path.join(dir, defaults.db_lifecycle_filename),args.output_file,args.target,"query")

@output._timer("SNMP Devices")
def snmp(search, args, dir):
    output.define_csv(args,search,queries.snmp_devices,os.path.join(dir, defaults.snmp_unrecognised_filename),args.output_file,args.target,"query")

@output._timer("Capture Candidates")
def capture_candidates(search, args, dir):
    results = search_results(search, queries.capture_candidates)
    count = len(results) if isinstance(results, list) else 0
    tools.completage("Processing", count or 1, (count or 1) - 1)
    print(os.linesep, end="\r")
    header, rows = [], []
    if isinstance(results, list) and results:
        header, rows, lookup = tools.json2csv(results, return_map=True)
        header = [lookup.get(h, h) for h in header]
        for row in rows:
            row.insert(0, args.target)
            # Replace ``None`` values with "N/A" for readability
            row[1:] = [value if value is not None else "N/A" for value in row[1:]]
    else:
        header, rows = [], []
    header.insert(0, "Discovery Instance")
    output.define_csv(
        args,
        header,
        rows,
        os.path.join(dir, defaults.capture_candidates_filename),
        args.output_file,
        args.target,
        "csv_file",
    )

@output._timer("Agents")
def agents(search, args, dir):
    output.define_csv(args,search,queries.agents,os.path.join(dir, defaults.installed_agents_filename),args.output_file,args.target,"query")

@output._timer("Expected Agents")
def expected_agents(search, args, dir):
    """Report hosts missing common agents via the API."""

    results = search_results(search, queries.agents)
    records = []
    for row in results:
        running = tools.getr(row, "Running_Software", "") or ""
        softwares = [s.strip() for s in running.split(";") if s.strip()]
        records.append({"Host_Name": tools.getr(row, "Host_Name", ""), "Running_Software": softwares})
    expected = common_agents.get_expected_agents(records)
    if expected:
        print("Expected agents: %s" % ", ".join(sorted(expected)))
    missing = common_agents.find_missing_agents(records, expected)
    data = [[rec["Host_Name"], ";".join(rec["Missing_Agents"])] for rec in missing]
    headers = ["Host Name", "Missing Agents"]
    output.report(data, headers, args, name="expected_agents")

@output._timer("Software Users")
def software_users(search, args, dir):
    output.define_csv(args,search,queries.user_accounts,os.path.join(dir, defaults.si_user_accounts_filename),args.output_file,args.target,"query")

def devices_lookup(search, include_network=False):
    """Return a mapping of IPs to their last discovery information.

    The device lookup previously relied on a single query to gather all data.
    The workflow now performs multiple queries to reduce the amount of data
    transferred and to allow callers to optionally request network details.

    1. ``deviceInfo_base`` seeds the mapping with host identity information.
    2. ``deviceInfo_access`` merges discovery metadata such as start times and
       results.
    3. When ``include_network`` is ``True``, ``deviceInfo_network`` is executed to
       attach additional network/IP details.

    Existing callers continue to receive the keys ``last_identity``,
    ``last_start_time``, and ``last_result``.  Network information, when
    requested, is stored under the ``network`` key.
    """

    # If the new granular queries are not available, fall back to the original
    # combined query to preserve compatibility with older deployments.
    if not (hasattr(queries, "deviceInfo_base") and hasattr(queries, "deviceInfo_access")):
        results = search_results(search, getattr(queries, "deviceInfo", {}))
        mapping = {}
        for result in results:
            ip = tools.getr(result, "DiscoveryAccess.endpoint", None)
            if ip:
                mapping[ip] = {
                    "last_identity": tools.getr(result, "DeviceInfo.hostname", "N/A"),
                    "last_start_time": tools.getr(result, "DiscoveryAccess.starttime", "N/A"),
                    "last_result": tools.getr(result, "DiscoveryAccess.result", "N/A"),
                }
        return mapping

    mapping = {}

    # Seed mapping with base device information.
    base_results = search_results(search, queries.deviceInfo_base)
    for result in base_results:
        ip = tools.getr(result, "DiscoveryAccess.endpoint", None)
        if ip:
            mapping[ip] = {
                "last_identity": tools.getr(result, "DeviceInfo.hostname", "N/A")
            }

    # Merge discovery access metadata.
    access_results = search_results(search, queries.deviceInfo_access)
    for result in access_results:
        ip = tools.getr(result, "DiscoveryAccess.endpoint", None)
        if ip:
            entry = mapping.setdefault(ip, {"last_identity": "N/A"})
            entry.update(
                {
                    "last_start_time": tools.getr(
                        result, "DiscoveryAccess.starttime", "N/A"
                    ),
                    "last_result": tools.getr(result, "DiscoveryAccess.result", "N/A"),
                }
            )

    # Optionally include network/IP details.
    if include_network and hasattr(queries, "deviceInfo_network"):
        network_results = search_results(search, queries.deviceInfo_network)
        for result in network_results:
            ip = tools.getr(result, "DiscoveryAccess.endpoint", None)
            if ip:
                entry = mapping.setdefault(ip, {"last_identity": "N/A"})
                entry.setdefault("network", {})
                entry["network"].update(
                    {
                        "ip_addrs": tools.getr(result, "NetworkInterface.ip_addr", [])
                    }
                )

    return mapping

def tku(knowledge, args, dir):
    logger.info("Checking Knowledge...")
    logger.debug("Calling knowledge.get_knowledge")
    api_response = knowledge.get_knowledge
    logger.debug(
        "knowledge.get_knowledge response ok=%s status=%s text=%s",
        getattr(api_response, "ok", "N/A"),
        getattr(api_response, "status_code", "N/A"),
        getattr(api_response, "text", "N/A"),
    )
    k = get_json(api_response)
    if k:
        result = json.loads(json.dumps(k))
        logger.debug('Knowledge:\n%s' % k)
        # Safely extract the latest uploads for each module, falling back to
        # "Not installed" when the key is missing.
        latest_edp = result.get('latest_edp', {}).get('name', 'Not installed')
        latest_storage = result.get('latest_storage', {}).get('name', 'Not installed')
        latest_tku = result.get('latest_tku', {}).get('name', 'Not installed')

        # Build rows for CSV output. Each row is prefixed with the Discovery
        # target so consumers know which appliance provided the data.
        rows = [
            [args.target, latest_tku],
            [args.target, latest_edp],
            [args.target, latest_storage],
        ]

        # Write a CSV file with a Discovery Instance and TKU columns.
        output.define_csv(
            args,
            ["Discovery Instance", "TKU"],
            rows,
            os.path.join(dir, defaults.tku_filename),
            args.output_file,
            args.target,
            "csv_file",
        )

def cancel_run(disco, args):
    run_id = args.a_kill_run
    logger.debug(
        "Calling disco.patch_discovery_run(%s, {cancelled: True})", run_id
    )
    cancel = disco.patch_discovery_run(run_id, {"cancelled": True})
    logger.debug(
        "disco.patch_discovery_run response ok=%s status=%s text=%s",
        getattr(cancel, "ok", "N/A"),
        getattr(cancel, "status_code", "N/A"),
        getattr(cancel, "text", "N/A"),
    )
    if cancel.ok:
        msg = "Cancelled Run %s.\n" % run_id
        print(msg)
        logger.info(msg)
        return cancel.ok
    elif 'message' in cancel.json():
        msg = cancel.json()['message'] + "\n"
        print(msg)
        logger.warning("Run not cancelled\n%s" % msg)
        return False
    else:
        msg = cancel.text + "\n"
        print(msg)
        logger.warning("Run not cancelled\n%s" % msg)
        return False

def update_schedule_timezone(disco, args):
    """Adjust discovery run start times for the given timezone."""
    tz = args.schedule_timezone
    reset = getattr(args, "reset_schedule_timezone", False)

    if not tz:
        logger.error("No timezone provided for schedule update")
        return

    from datetime import datetime
    from zoneinfo import ZoneInfo

    # Allow a few common short names
    common = {
        "UTC": 0,
        "CST": -6,
        "CDT": -5,
        "EST": -5,
        "EDT": -4,
        "PST": -8,
        "PDT": -7,
        "MST": -7,
        "MDT": -6,
    }

    try:
        if tz.upper() in common:
            offset = common[tz.upper()]
        else:
            offset = int(
                (datetime.now(ZoneInfo(tz)).utcoffset() or datetime.timedelta())
                .total_seconds()
                // 3600
            )
    except Exception as e:
        msg = f"Invalid timezone {tz}: {e}"
        print(msg)
        logger.error(msg)
        return

    if reset:
        offset = -offset

    logger.debug("Calling disco.get_discovery_runs")
    api_response = disco.get_discovery_runs
    logger.debug(
        "disco.get_discovery_runs response ok=%s status=%s text=%s",
        getattr(api_response, "ok", "N/A"),
        getattr(api_response, "status_code", "N/A"),
        getattr(api_response, "text", "N/A"),
    )

    runs = get_json(api_response)
    if not runs:
        logger.error("No discovery runs returned")
        return

    for run in runs:
        run_id = run.get("range_id") or run.get("id") or run.get("run_id")
        schedule = run.get("schedule", {})
        start_times = schedule.get("start_times", [])
        if not run_id or not isinstance(start_times, list):
            continue
        new_times = [int((t + offset) % 24) for t in start_times]
        patch = {"schedule": {"start_times": new_times}}
        logger.debug("Calling disco.patch_discovery_run(%s, %s)", run_id, patch)
        resp = disco.patch_discovery_run(run_id, patch)
        logger.debug(
            "disco.patch_discovery_run response ok=%s status=%s text=%s",
            getattr(resp, "ok", "N/A"),
            getattr(resp, "status_code", "N/A"),
            getattr(resp, "text", "N/A"),
        )

def vault(vault, args, dir):
    logger.info("Checking Vault...")
    logger.debug("Calling vault.get_vault")
    api_response = vault.get_vault
    logger.debug(
        "vault.get_vault response ok=%s status=%s text=%s",
        getattr(api_response, "ok", "N/A"),
        getattr(api_response, "status_code", "N/A"),
        getattr(api_response, "text", "N/A"),
    )
    v = get_json(api_response)
    if v:
        result = json.loads(json.dumps(v))
        logger.debug('Vault Status:\n%s'%v)
        vopen = result.get('open')
        vsaved = result.get('passphrase_saved')
        vset = result.get('passphrase_set')
        vault_status = "OK"
        if not vopen:
            if not vsaved:
                vault_status = "Vault closed - Passphrase not saved"
        if not vset:
            vault_status = "Vault open - no passphrase set"
        output.define_txt(args,vault_status,os.path.join(dir, defaults.vault_filename),None)

def remove_cred(appliance, cred):
    logger.debug("Calling appliance.delete_vault_credential(%s)", cred)
    delete = appliance.delete_vault_credential(cred)
    logger.debug(
        "delete_vault_credential response ok=%s status=%s text=%s",
        getattr(delete, "ok", "N/A"),
        getattr(delete, "status_code", "N/A"),
        getattr(delete, "text", "N/A"),
    )
    if delete.ok:
        msg = "Credential UUID %s deleted.\n" % cred
        print(msg)
        logger.info(msg)
        return delete.ok
    elif 'message' in delete.json():
        msg = delete.json()['message'] + "\n"
        print(msg)
        logger.warning("Credential not deleted\n%s" % msg)
        return False
    else:
        msg = delete.text + "\n"
        print(msg)
        logger.warning("Credential not deleted\n%s" % msg)
        return False

def update_cred(appliance, uuid):
    logger.debug("Calling appliance.get_vault_credential(%s)", uuid)
    lookup = appliance.get_vault_credential(uuid)
    logger.debug(
        "get_vault_credential response ok=%s status=%s text=%s",
        getattr(lookup, "ok", "N/A"),
        getattr(lookup, "status_code", "N/A"),
        getattr(lookup, "text", "N/A"),
    )
    lookupjson = get_json(lookup)
    if 'message' in lookupjson:
        enabled = None
        msg = lookupjson.get('message')
        print(msg)
        logger.warning("Credential not updated\n%s" % msg)
    else:
        enabled = lookupjson.get('enabled')
    active = None
    if enabled is not None:
        if enabled:
            logger.debug(
                "Calling appliance.patch_vault_credential(%s, {enabled: False})",
                uuid,
            )
            resp = appliance.patch_vault_credential(uuid,{"enabled":False})
            logger.debug(
                "patch_vault_credential response ok=%s status=%s text=%s",
                getattr(resp, "ok", "N/A"),
                getattr(resp, "status_code", "N/A"),
                getattr(resp, "text", "N/A"),
            )
            active = False
        else:
            logger.debug(
                "Calling appliance.patch_vault_credential(%s, {enabled: True})",
                uuid,
            )
            resp = appliance.patch_vault_credential(uuid,{"enabled":True})
            logger.debug(
                "patch_vault_credential response ok=%s status=%s text=%s",
                getattr(resp, "ok", "N/A"),
                getattr(resp, "status_code", "N/A"),
                getattr(resp, "text", "N/A"),
            )
            active = True
    return active

def search_results(
    api_endpoint,
    query,
    limit=500,
    use_cache=True,
    cache_name=None,
    page_size=500,
):
    """Execute a search query and return all results.

    The Discovery API defaults to returning a maximum of 500 rows per request.
    Older versions of :func:`search_results` mirrored this behaviour which
    meant callers could silently miss data when more than 500 rows were
    available.  The ``limit`` parameter allows callers to specify a custom
    limit or pass ``0`` to retrieve *all* available rows via pagination.  The
    ``page_size`` parameter controls how many rows are requested per page and
    defaults to ``500``.  This value may be automatically reduced when the
    appliance repeatedly returns ``504`` errors.

    Results are cached based on the ``query`` and ``limit`` parameters.  Set
    ``use_cache`` to ``False`` to bypass the cache and force a fresh API call.
    """

    try:
        use_cache = use_cache and cache.is_enabled()
        query = cache.canonical_query(query)
        if isinstance(query, dict) and isinstance(query.get("query"), str):
            # ``canonical_query`` returns a shallow copy so it is safe to mutate
            query = dict(query)
        if logger.isEnabledFor(logging.DEBUG):
            try:
                logger.debug("Search query: %s" % query)
            except Exception:
                pass

        # Reset cache when querying a different API endpoint
        global _CACHE_ENDPOINT
        if _CACHE_ENDPOINT is not api_endpoint:
            _SEARCH_CACHE.clear()
            _CACHE_ENDPOINT = api_endpoint

        # Build a hashable cache key from the query and limit
        key_query = json.dumps(query, sort_keys=True, default=str)
        cache_key = (key_query, limit)
        if use_cache and cache_key in _SEARCH_CACHE:
            return _SEARCH_CACHE[cache_key]
        if use_cache:
            cached = cache.load(cache_name or "query", query, limit)
            if cached is not None:
                _SEARCH_CACHE[cache_key] = cached
                return cached

        # Determine the page size for each request.  A limit of ``0`` denotes
        # no limit which we implement by requesting data in ``page_size`` row
        # chunks until the API stops returning additional results.
        results_all = []
        page_limit = page_size if not limit or limit > page_size else limit
        offset = 0
        remaining = limit

        while True:
            kwargs = {"format": "object", "limit": page_limit}
            if offset:
                kwargs["offset"] = offset

            # Perform the search, retrying on 504 Gateway Timeout errors
            max_retries = 3
            while True:
                for attempt in range(max_retries):
                    if hasattr(api_endpoint, "search_bulk"):
                        try:
                            results = api_endpoint.search_bulk(query, **kwargs)
                        except TypeError:  # pragma: no cover - older libs lack offset
                            kwargs.pop("offset", None)
                            results = api_endpoint.search_bulk(query, **kwargs)
                            offset = 0
                    else:
                        try:
                            results = api_endpoint.search(query, **kwargs)
                        except TypeError:  # pragma: no cover - older libs lack offset
                            kwargs.pop("offset", None)
                            results = api_endpoint.search(query, **kwargs)
                            offset = 0

                    status_code = getattr(results, "status_code", 200)
                    if status_code != 504:
                        break
                    if attempt < max_retries - 1:
                        logger.warning(
                            "Search API returned 504 - Gateway Timeout. Retrying (%s/%s)...",
                            attempt + 1,
                            max_retries,
                        )
                        time.sleep(2 ** attempt)
                else:
                    if page_limit > 1:
                        new_limit = max(1, page_limit // 2)
                        logger.warning(
                            "Reducing page limit from %s to %s due to repeated 504 errors",
                            page_limit,
                            new_limit,
                        )
                        page_limit = new_limit
                        kwargs["limit"] = page_limit
                        continue
                    raise APITimeoutError(
                        "Search API returned 504 - Gateway Timeout after multiple retries"
                    )
                break

            # Depending on the version of the `tideway` library the call above
            # may return either a `requests.Response` object or the decoded
            # JSON directly.  Normalise the output so callers always get Python
            # data structures.
            if hasattr(results, "json"):
                if logger.isEnabledFor(logging.DEBUG):
                    try:
                        logger.debug("Raw search response: %s" % results.text)
                    except Exception:
                        pass
                status_code = getattr(results, "status_code", 200)
                if status_code >= 400:
                    logger.error(
                        "Search API returned %s - %s",
                        status_code,
                        getattr(results, "reason", ""),
                    )
                    if status_code >= 500:
                        reason = getattr(results, "reason", "") or "server error"
                        # Highlight server-side failures so users know results may
                        # not reflect the full dataset.
                        if status_code == 504:
                            msg_reason = "timed out"
                        else:
                            msg_reason = reason.lower()
                        warning_msg = (
                            f"*** WARNING: Search API {msg_reason} ({status_code}). "
                            "Results may be incomplete. ***"
                        )
                        print(warning_msg)
                    try:
                        data = json.loads(results.text)
                    except Exception:
                        data = {"error": getattr(results, "text", "")}
                    if logger.isEnabledFor(logging.DEBUG):
                        try:
                            logger.debug("Parsed error payload: %s", json.dumps(data))
                        except Exception:
                            pass
                    logger.error(
                        "Search failed: %s - %s", status_code, getattr(results, "reason", "")
                    )
                    if use_cache:
                        cache.save(cache_name or "query", query, limit, data)
                        _SEARCH_CACHE[cache_key] = data
                    return data
                try:
                    data = results.json()
                except Exception as e:
                    msg = "Error decoding JSON from search results: %s" % str(e)
                    print(msg)
                    logger.error(msg)
                    return []
                if isinstance(data, dict) and isinstance(data.get("results"), list):
                    data = dict(data)
                    data["results"] = tools.list_table_to_json(data["results"])
            else:
                data = results
            if logger.isEnabledFor(logging.DEBUG):
                try:
                    logger.debug("Parsed results length: %s" % len(data))
                except Exception:
                    pass

            # ``data`` is expected to be a list of rows.  If not, return it
            # directly so callers can handle error objects consistently.
            if not isinstance(data, list):
                if isinstance(data, dict) and isinstance(data.get("results"), list):
                    # Normalise embedded table results
                    data = dict(data)
                    data["results"] = tools.list_table_to_json(data["results"])
                    if use_cache:
                        cache.save(cache_name or "query", query, limit, data)
                        _SEARCH_CACHE[cache_key] = data
                    return data
                if use_cache:
                    cache.save(cache_name or "query", query, limit, data)
                    _SEARCH_CACHE[cache_key] = data
                return data

            results_all.extend(data)
            
            # If limit==0 and the server already returned more rows than requested,
            # treat this as the complete result set and exit.
            if not limit and offset == 0 and len(data) > page_limit:
                break

            # Stop when we've retrieved the requested number of rows or when
            # the API returns fewer rows than requested for a given page.
            if limit and limit > 0 and len(results_all) >= limit:
                results_all = results_all[:limit]
                break
            if len(data) < page_limit:
                break
            offset += page_limit
            if limit and limit > 0:
                remaining = limit - len(results_all)
                if remaining <= 0:
                    break
                page_limit = page_size if remaining > page_size else remaining

        result_json = tools.list_table_to_json(results_all)
        if use_cache:
            _SEARCH_CACHE[cache_key] = result_json
            cache.save(cache_name or "query", query, limit, result_json)
        return result_json
    except APITimeoutError:
        raise
    except Exception as e:
        if logger.isEnabledFor(logging.DEBUG):
            msg = (
                "Not able to make api call.\nQuery: %s\nException: %s\n%s"
                % (query, e.__class__, str(e))
            )
            print(msg)
            logger.error(msg)
        else:
            msg = "Not able to make api call. Rerun in debug mode for more information."
            print(msg)
            logger.error(
                "Not able to make api call for query %s", query, exc_info=e
            )
        return []

def search_in_chunks(
    api_endpoint,
    base_query,
    chunks,
    *,
    limit=0,
    use_cache=True,
    cache_name="chunk",
    page_size=500,
):
    """Run a query multiple times using a chunking strategy.

    Parameters
    ----------
    api_endpoint
        The search endpoint object used for API calls.
    base_query : str | dict
        Query template applied to each chunk.  If a dictionary is supplied
        the ``"query"`` key is formatted.
    chunks : iterable
        Sequence of values used to tailor the query for each iteration.  Each
        element is passed to :func:`str.format` on ``base_query``.  When an
        element is a mapping the values are expanded as named fields.
    limit : int, optional
        Passed directly to :func:`search_results`.  Defaults to ``0`` which
        retrieves all results for each chunk.
    use_cache : bool, optional
        Whether to utilise the on-disk cache.
    cache_name : str, optional
        Prefix for cache entries.  A unique suffix is appended for every
        chunk so results are stored separately.
    page_size : int, optional
        Maximum number of rows requested per API call.  Passed directly to
        :func:`search_results`.

    Returns
    -------
    list
        Combined results from all chunks.  Non-list responses from
        ``search_results`` are appended as-is allowing callers to inspect
        error payloads.
    """

    combined = []
    for idx, chunk in enumerate(chunks):
        if isinstance(base_query, dict):
            query = dict(base_query)
            qstring = query.get("query", "")
            if isinstance(chunk, dict):
                query["query"] = qstring.format(**chunk)
            else:
                query["query"] = qstring.format(chunk)
        else:
            if isinstance(chunk, dict):
                query = base_query.format(**chunk)
            else:
                query = base_query.format(chunk)

        chunk_cache = f"{cache_name}-{idx}"
        result = search_results(
            api_endpoint,
            query,
            limit=limit,
            use_cache=use_cache,
            cache_name=chunk_cache,
            page_size=page_size,
        )
        if isinstance(result, list):
            combined.extend(result)
        else:
            combined.append(result)
    return combined


def _parse_export_data(data):
    """Return rows from exported search data.

    The ``data`` parameter may be a response object or a plain string.  The
    content is inspected and parsed as JSON when possible, otherwise treated as
    CSV.  A list of row dictionaries is returned in all cases.
    """

    text = getattr(data, "text", data)
    if isinstance(text, bytes):
        text = text.decode()
    if not isinstance(text, str):
        return []

    text = text.strip()
    if not text:
        return []

    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict) and isinstance(parsed.get("results"), list):
            return parsed["results"]
        if isinstance(parsed, list):
            return parsed
    except Exception:
        pass

    reader = csv.DictReader(io.StringIO(text))
    return [row for row in reader]


def export_search(api_endpoint, query, *, poll_interval=2, timeout=300):
    """Execute a search export and return the resulting rows.

    This function uses the asynchronous export API to retrieve data for heavy
    queries.  The search job is polled until completion before downloading and
    parsing the results.
    """

    payload = query if isinstance(query, dict) else {"query": query}
    job = api_endpoint.export(payload)
    info = get_json(job)
    export_id = (
        info.get("export_id")
        or info.get("job_id")
        or info.get("id")
    )
    if not export_id:
        logger.error("Export response missing job identifier: %s", info)
        return []

    start = time.time()
    while True:
        status_resp = api_endpoint.export_status(export_id)
        status = get_json(status_resp)
        state = str(status.get("status") or status.get("state") or "").lower()
        if state in {"completed", "complete", "done", "finished", "success", "succeeded"}:
            break
        if state in {"failed", "error"}:
            logger.error("Export job failed: %s", status)
            return []
        if time.time() - start > timeout:
            logger.error("Export job timed out after %s seconds", timeout)
            return []
        time.sleep(poll_interval)

    file_resp = api_endpoint.export_download(export_id)
    return _parse_export_data(file_resp)

REPORT_QUERY_MAP = {
    "credential_success": [
        "credential_success",
        "deviceinfo_success",
        "credential_failure",
        "credential_success_7d",
        "deviceinfo_success_7d",
        "credential_failure_7d",
        "scanrange",
        "excludes",
        "outpost_credentials",
    ],
    # The device_ids report uses a dedicated query
    "device_ids": ["device_ids"],
  
    # The devices report uses granular deviceInfo queries
    "devices": [
        "deviceInfo_base",
        "deviceInfo_access",
        "deviceInfo_network",
    ],
}

def run_queries(search, args, dir):
    """Execute queries from :mod:`core.queries` without post-processing.

    This utility looks up each name provided via ``args.excavate`` in the
    :mod:`core.queries` module, runs the raw query against the API and saves the
    results to CSV.  Each file is written to ``dir`` and prefixed with
    ``qry_`` so users can inspect the unmodified output from the appliance.
    """

    names = getattr(args, "excavate", []) or []
    for name in names:
        for qname in REPORT_QUERY_MAP.get(name, [name]):
            query = getattr(queries, qname, None)
            if query is None:
                msg = f"Query '{qname}' not found"
                print(msg)
                logger.error(msg)
                continue

            filename = os.path.join(dir, f"qry_{qname}.csv")
            # Use the "query" output type so ``define_csv`` handles the API call
            # and CSV conversion for us without additional processing.
            output.define_csv(
                args,
                search,
                query,
                filename,
                getattr(args, "output_file", None),
                getattr(args, "target", None),
                "query",
                query_name=qname,
            )

def hostname(args,dir):
    output.define_txt(args,args.target,os.path.join(dir, defaults.hostname_filename),None)
