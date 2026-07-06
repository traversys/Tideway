# Transformation tools for DisMAL

import logging
import re
from platform import uname

# PIP Modules
import ipaddress
from cidrize import cidrize

logger = logging.getLogger("_tools_")

def in_wsl() -> bool:
    """
        WSL is thought to be the only common Linux kernel with Microsoft in the name, per Microsoft:
        https://github.com/microsoft/WSL/issues/4071#issuecomment-496715404
    """
    return 'Microsoft' in uname().release

def getr(data, attribute, default_value=None):
    """Return ``data[attribute]`` if present, else ``default_value``.

    This avoids treating falsy values like ``0`` or ``""`` as missing.
    """
    return data[attribute] if attribute in data else default_value

def range_to_ips(iprange):
    """Return a list of :class:`ipaddress.IPv4Network`/`IPv6Network` objects.

    The previous implementation expanded ranges into individual IP addresses
    which was expensive for large networks.  This helper now preserves the
    ranges and returns ``ip_network`` objects instead.  Cloud end points and
    the special "all" range are returned unchanged as strings.
    """

    networks = []
    logger.info("Running range_to_ips function on %s" % iprange)
    if not iprange:
        return networks

    if re.search("[a-zA-Z]", iprange):
        logger.debug("IP range is cloud endpoint!")
        networks.append(iprange)
    elif iprange == "0.0.0.0/0,::/0":
        networks.append(iprange)
        logger.debug("All - List of Networks: %s" % networks)
    else:
        parts = [ip for ip in iprange.split(",") if ip]
        for ip in parts:
            try:
                net = ipaddress.ip_network(ip, strict=False)
                networks.append(net)
                logger.debug("Network appended: %s", net)
            except Exception:
                try:
                    cidrip = cidrize(ip)
                    for cidr in cidrip:
                        net = ipaddress.ip_network(cidr, strict=False)
                        networks.append(net)
                        logger.debug("CIDRize - Network appended: %s", net)
                except Exception:
                    msg = "Address %s is not valid CIDR syntax, cannot process!" % ip
                    print(msg)
                    logger.warning(msg)
    return networks

def get_credential(data,uuid):
    credentials = data
    detail = {}
    for credential in credentials:
        if uuid == credential.get('uuid'):
            uuid = getr(credential,'uuid')
            index = getr(credential,'index')
            label = getr(credential,'label')
            enabled = getr(credential,'enabled')
            types = getr(credential,'types')
            username = None
            if 'username' in credential:
                username = getr(credential,'username')
            elif 'snmp.v3.securityname' in credential:
                username = getr(credential,'snmp.v3.securityname')
            elif 'aws.access_key_id' in credential:
                username = getr(credential,'aws.access_key_id')
            elif 'azure.application_id' in credential:
                username = getr(credential,'azure.application_id')
            iprange = getr(credential,'ip_range')
            exclusions = getr(credential,'ip_exclusion')
            detail = {"index":index,"uuid":uuid,"label":label,"username":username,"enabled":enabled,"iprange":iprange,"exclusions":exclusions,"types":types}
    return detail

def sortlist(lst,dv=None):
    logger.debug("List to sort and unique:\n%s"%lst)
    if dv:
        logger.debug("Replace None values with %s"%dv)
        lst = [ dv if v is None else v for v in lst ] # replace None values
    else:
        logger.debug("Remove None values")
        lst = [ v for v in lst if v is not None ] # remove None values
    lst = sorted(set(lst)) # sort and unique
    logger.debug(lst)
    return lst

def sortdic(lst):
    logger.debug("Dict to sort and unique:\n%s"%lst)
    lst2 = [i for n, i in enumerate(lst) if i not in lst[n + 1:]]
    logger.debug(lst)
    return lst2

def completage(message, record_count, timer_count):
    timer_count += 1
    pc = (float(timer_count) / float(record_count))
    if timer_count >= record_count:
        end_char = '\n'
    else:
        end_char = '\r'
    print('%s: %d%%' % (message,100.0 * pc), end=end_char)
    return timer_count

def list_of_lists(ci,attr,list_to_append):
    thing = ci.get(attr)
    if type(ci.get(attr)) is list:
        for item in thing:
            if type(item) is list:
                for sub_item in item:
                    list_to_append.append(sub_item)
            else:
                list_to_append.append(item)
    else:
        list_to_append.append(thing)
    return list_to_append

def session_get(results):
    """Convert session/device info search results into a mapping.

    Results may contain ``SessionResult.credential_or_slave`` (or the legacy
    ``SessionResult.slave_or_credential``), ``DeviceInfo.last_credential`` or a
    generic ``uuid`` field.  Any object
    path prefixes are stripped so the returned dictionary uses raw credential
    UUIDs as keys.  The stored value is a two-item list of the access method and
    lookup count.

    Previous implementations assumed ``results`` was always a list of
    dictionaries returned from the search API.  When the API call failed (for
    example with a 504 gateway timeout) a string or dictionary was supplied
    instead which caused attribute errors when attempting to access ``get`` on
    a non-dict object.  This helper now defensively checks input types and
    gracefully skips any malformed entries.
    """

    sessions = {}

    if isinstance(results, dict):
        results = results.get("results", [])

    # Some API endpoints return tabular data as a list of lists where the
    # first row contains headers.  Normalize this format into a list of
    # dictionaries before processing so the function can operate on either
    # representation transparently.
    if isinstance(results, list) and results and isinstance(results[0], list):
        results = list_table_to_json(results)

    if not isinstance(results, list):
        logger.warning(
            "session_get expected list of results, got %s", type(results).__name__
        )
        logger.debug("session_get received payload: %r", results)
        return sessions

    for result in results:
        if not isinstance(result, dict):
            logger.warning("session_get skipping non-dict result: %r", result)
            continue

        # Cast count values to integers to ensure arithmetic works as expected
        try:
            count = int(result.get("Count", 0) or 0)
        except (TypeError, ValueError):
            count = 0

        # Accept both SessionResult and DeviceInfo credential fields, falling
        # back to a plain ``uuid`` field if neither is present.
        uuid = (
            result.get("SessionResult.credential_or_slave")
            or result.get("SessionResult.slave_or_credential")
            or result.get("DeviceInfo.last_credential")
            or result.get("uuid")
        )

        # Pull the access/session type from whichever query populated the row
        restype = result.get("SessionResult.session_type") or result.get(
            "DeviceInfo.access_method"
        )

        if uuid:
            # Normalize credential identifiers: drop any object-path prefixes
            # and perform case-insensitive comparisons by storing the UUID in
            # lowercase. Casting to ``str`` also protects against UUID objects
            # from third-party libraries.
            uuid = str(uuid).split("/")[-1].lower()
            sessions[uuid] = [restype, count]

    return sessions

def ip_or_string(value):
    try:
        ip = int(ipaddress.ip_address(value))
        msg = "Value %s converted to IPAddress %s."%(value,ip)
        logger.debug(msg)
        return ip
    except ValueError:
        msg = "Value %s Could not be convered to IPAddress"%value
        logger.warning(msg)
        return value

def extract_credential(entry):
    details = {}
    uuid = entry.get('uuid')
    index = entry.get('index')
    label = entry.get('label')
    enabled = entry.get('enabled')
    types = entry.get('types')
    usage = entry.get('usage')
    internal_store = entry.get('internal.store')
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
    details = {"index":index,"uuid":uuid,"label":label,"username":username,"enabled":enabled,"iprange":iprange,"exclusions":exclusions,"types":types,"usage":usage,"internal_store":internal_store}
    return details

def dequote(s):
    """
    If a string has double quotes around it, remove them.
    Make sure the pair of quotes match.
    If a matching pair of quotes is not found, return the string unchanged.
    """
    if (s[0] == s[-1]) and s.startswith('"'):
        return s[1:-1]
    return s


def json2csv(jsdata, return_map=False):
    header = []
    data = []
    for jsitem in jsdata:
        for label in jsitem.keys():
            header.append(label)
            header = sortlist(header)

    for jsitem in jsdata:
        values = []
        for key in header:
            values.append(getr(jsitem, key, "N/A"))
        data.append(values)

    lookup = {h: h for h in header}
    if return_map:
        lookup = {h: h for h in header}
        return header, data, lookup

    return header, data, header

def snake_to_title(value):
    """Convert ``snake_case`` strings to Title Case with spaces.

    Common abbreviations such as ``os`` and ``id`` are preserved in uppercase.
    Non-string values or already formatted labels are returned unchanged.
    """
    if not isinstance(value, str):
        return value

    if not value.islower():
        return value

    abbreviations = {"os": "OS", "id": "ID"}
    parts = value.split("_")
    words = []
    for part in parts:
        if part in abbreviations:
            words.append(abbreviations[part])
            continue
        for abbr, repl in abbreviations.items():
            if part.endswith(abbr) and part != abbr:
                prefix = part[:-len(abbr)]
                if prefix:
                    words.append(prefix.capitalize())
                words.append(repl)
                break
        else:
            words.append(part.capitalize())
    return " ".join(words)

def list_table_to_json(rows):
    """Convert a list-of-lists table to a list of dictionaries.

    The first row is treated as headers.  If ``rows`` is not a list of
    lists, the value is returned unchanged.
    """
    if isinstance(rows, list) and rows and isinstance(rows[0], list):
        headers = rows[0]
        return [dict(zip(headers, r)) for r in rows[1:]]
    return rows

