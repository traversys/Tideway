"""Host software inventory and agent coverage for Discovery notebooks."""

from collections import defaultdict


HOST_SOFTWARE_QUERY = """search Host
where os_type has subword 'Windows' or os_type has subword 'Linux'
show
    #id as 'Host ID',
    name as 'Host Name',
    os_type as 'OS Type',
    last_update_success as 'Last Successful Scan',
    #HostedSoftware:RunningSoftware:SoftwareInstance.type as 'Software Types'
"""


def _software_types(value):
    if isinstance(value, (list, tuple, set)):
        return {str(item).strip() for item in value if str(item).strip()}
    if isinstance(value, str):
        return {item.strip() for item in value.split(";") if item.strip()}
    return set()


def normalise_hosts(rows):
    """Keep one inventory record per host and OS, with distinct software types."""
    hosts = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        name = str(row.get("Host Name") or "").strip()
        os_type = str(row.get("OS Type") or "").strip()
        family = "Windows" if "windows" in os_type.lower() else "Linux" if "linux" in os_type.lower() else None
        if not name or not family:
            continue
        host_id = str(row.get("Host ID") or name).strip()
        key = (family, host_id)
        if key not in hosts:
            hosts[key] = {
                "Host ID": host_id,
                "Host Name": name,
                "OS Family": family,
                "Last Successful Scan": row.get("Last Successful Scan"),
                "Software Types": set(),
            }
        hosts[key]["Software Types"].update(_software_types(row.get("Software Types")))
    return list(hosts.values())


def software_coverage(hosts):
    """Count each software type at most once per host, by OS family."""
    totals = defaultdict(int)
    counts = defaultdict(int)
    for host in hosts:
        family = host["OS Family"]
        totals[family] += 1
        for software in host["Software Types"]:
            counts[(family, software)] += 1
    return [
        {
            "OS Family": family,
            "Software Type": software,
            "Hosts Present": present,
            "Hosts Total": totals[family],
            "Hosts Missing": totals[family] - present,
            "Coverage": present / totals[family],
        }
        for (family, software), present in sorted(counts.items())
    ]


def compliance_rows(hosts, requirements):
    """Find missing customer-approved software names using exact type matching."""
    rows = []
    for host in hosts:
        observed = {software.casefold() for software in host["Software Types"]}
        for required in requirements.get(host["OS Family"], []):
            required = required.strip()
            if required and required.casefold() not in observed:
                rows.append({
                    "Host ID": host["Host ID"],
                    "Host Name": host["Host Name"],
                    "OS Family": host["OS Family"],
                    "Missing Software": required,
                    "Last Successful Scan": host["Last Successful Scan"],
                })
    return rows
