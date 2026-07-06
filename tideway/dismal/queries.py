# Discovery API queries for DisMAL

credential_success = """
                            search SessionResult where success
                            show (credential or slave) as 'SessionResult.credential_or_slave',
                            (credential or slave) as 'uuid',
                            session_type as 'SessionResult.session_type',
                            outpost as 'SessionResult.outpost'
                            processwith countUnique(1,0)
                        """
credential_failure = """
                            search SessionResult where not success
                            show (credential or slave) as 'SessionResult.credential_or_slave',
                            (credential or slave) as 'uuid',
                            session_type as 'SessionResult.session_type',
                            outpost as 'SessionResult.outpost'
                            processwith countUnique(1,0)
                        """
deviceinfo_success = """
                          search DeviceInfo where method_success
                          and nodecount(traverse DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess
                                            traverse DiscoveryAccess:Metadata:Detail:SessionResult) = 0
                          show (last_credential or last_slave) as 'DeviceInfo.last_credential',
                          (last_credential or last_slave) as 'uuid',
                          access_method as 'DeviceInfo.access_method'
                          process with countUnique(1,0)
                       """
credential_success_7d = """
                            search SessionResult where success and time_index > (currentTime() - 7*24*3600*10000000)
                            show (credential or slave) as 'SessionResult.credential_or_slave',
                            (credential or slave) as 'uuid',
                            session_type as 'SessionResult.session_type',
                            outpost as 'SessionResult.outpost'
                            processwith countUnique(1,0)
                        """
credential_failure_7d = """
                            search SessionResult where not success and time_index > (currentTime() - 7*24*3600*10000000)
                            show (credential or slave) as 'SessionResult.credential_or_slave',
                            (credential or slave) as 'uuid',
                            session_type as 'SessionResult.session_type',
                            outpost as 'SessionResult.outpost'
                            processwith countUnique(1,0)
                        """
deviceinfo_success_7d = """
                          search DeviceInfo where method_success
                          and nodecount(traverse DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess
                                            traverse DiscoveryAccess:Metadata:Detail:SessionResult) = 0
                          and time_index > (currentTime() - 7*24*3600*10000000)
                          show (last_credential or last_slave) as 'DeviceInfo.last_credential',
                          (last_credential or last_slave) as 'uuid',
                          access_method as 'DeviceInfo.access_method'
                          process with countUnique(1,0)
                       """
outpost_credentials = """
                            search SessionResult
                            show credential,
                            credential as 'uuid',
                            outpost
                            process with unique(0)
                        """
deviceInfo_base = {"query":
                        """
                            search DeviceInfo
                            ORDER BY hostname
                            show
                            hostname as 'DeviceInfo.hostname',
                            os_type as 'DeviceInfo.os_type',
                            sysname as 'DeviceInfo.sysname',
                            device_type as 'DeviceInfo.device_type',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.endpoint as 'DiscoveryAccess.endpoint',
                            fqdn as 'DeviceInfo.fqdn',
                            kind as 'DeviceInfo.kind',
                            method_success as 'DeviceInfo.method_success',
                            method_failure as 'DeviceInfo.method_failure',
                            (last_credential or last_slave or __preserved_last_credential) as 'DeviceInfo.last_credential',
                            (last_access_method or __preserved_last_access_method) as 'DeviceInfo.last_access_method'
                            process with unique()
                        """
                }
deviceInfo = {"query":
                        """
                            search DeviceInfo
                            ORDER BY hostname
                            show
                            hostname as 'DeviceInfo.hostname',
                            hash(hostname) as 'DeviceInfo.hashed_hostname',
                            os_type as 'DeviceInfo.os_type',
                            sysname as 'DeviceInfo.sysname',
                            device_type as 'DeviceInfo.device_type',
                            fqdn as 'DeviceInfo.fqdn',
                            method_success as 'DeviceInfo.method_success',
                            method_failure as 'DeviceInfo.method_failure',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.#::InferredElement:.name as 'InferredElement.name',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.#::InferredElement:.hostname as 'InferredElement.hostname',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.#::InferredElement:.local_fqdn as 'InferredElement.local_fqdn',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.#::InferredElement:.sysname as 'InferredElement.sysname',
                            kind as 'DeviceInfo.kind',
                            (last_credential or last_slave or __preserved_last_credential) as 'DeviceInfo.last_credential',
                            (last_access_method or __preserved_last_access_method) as 'DeviceInfo.last_access_method',
                            friendlyTime(#DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.starttime) as 'DiscoveryAccess.starttime',
                            friendlyTime(#DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.endtime) as 'DiscoveryAccess.endtime',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.result as 'DiscoveryAccess.result',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.endpoint as 'DiscoveryAccess.endpoint',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.end_state as 'DiscoveryAccess.end_state',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.#DiscoveryAccess:Endpoint:Endpoint:Endpoint.endpoint as 'Endpoint.endpoint',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.#DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DiscoveredIPAddressList.#List:List:Member:DiscoveredIPAddress.ip_addr as 'DiscoveredIPAddress.ip_addr',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.#::InferredElement:.__all_ip_addrs as 'InferredElement.__all_ip_addrs',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.#::InferredElement:.#DeviceWithInterface:DeviceInterface:InterfaceOfDevice:NetworkInterface.ip_addr as 'NetworkInterface.ip_addr',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.#::InferredElement:.#DeviceWithInterface:DeviceInterface:InterfaceOfDevice:NetworkInterface.fqdns as 'NetworkInterface.fqdns',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.#Member:List:List:DiscoveryRun.label as 'DiscoveryRun.label',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess._last_marker as 'DiscoveryAccess._last_marker',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess._first_marker as 'DiscoveryAccess._first_marker',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess._last_interesting as 'DiscoveryAccess._last_interesting',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.__had_inference as 'DiscoveryAccess.__had_inference'
                            process with unique()
                        """
                }

deviceInfo_network = {
                        "query":
                            """
                                search DeviceInfo
                                ORDER BY hostname
                                show
                                hostname as 'DeviceInfo.hostname',
                                #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.endpoint as 'DiscoveryAccess.endpoint',
                                #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.#DiscoveryAccess:Endpoint:Endpoint:Endpoint.endpoint as 'Endpoint.endpoint',
                                #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.#::InferredElement:.__all_ip_addrs as 'InferredElement.__all_ip_addrs',
                                #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.#::InferredElement:.#DeviceWithInterface:DeviceInterface:InterfaceOfDevice:NetworkInterface.ip_addr as 'NetworkInterface.ip_addr',
                                #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.#::InferredElement:.#DeviceWithInterface:DeviceInterface:InterfaceOfDevice:NetworkInterface.fqdns as 'NetworkInterface.fqdns',
                                #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.#DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DiscoveredIPAddressList.#List:List:Member:DiscoveredIPAddress.ip_addr as 'DiscoveredIPAddress.ip_addr'
                                process with unique()
                            """
                }

deviceInfo_access = {
                    "query":
                        """
                            search DeviceInfo
                            show
                            hostname as 'DeviceInfo.hostname',
                            friendlyTime(#DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.starttime) as 'DiscoveryAccess.starttime',
                            friendlyTime(#DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.endtime) as 'DiscoveryAccess.endtime',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.result as 'DiscoveryAccess.result',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.endpoint as 'DiscoveryAccess.endpoint',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.end_state as 'DiscoveryAccess.end_state',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess._last_marker as 'DiscoveryAccess._last_marker',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess._first_marker as 'DiscoveryAccess._first_marker',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess._last_interesting as 'DiscoveryAccess._last_interesting',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.#Member:List:List:DiscoveryRun.label as 'DiscoveryRun.label',
                            #DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.__had_inference as 'DiscoveryAccess.__had_inference'
                            process with unique()
                        """
                    }

da_ip_lookup = {
                    "query":
                            """
                                search DiscoveryAccess
                                show
                                endpoint as 'DiscoveryAccess.endpoint',
                                hash(endpoint) as 'DiscoveryAccess.hashed_endpoint',
                                #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.hostname as 'DeviceInfo.hostname',
                                (#DiscoveryAccess:Metadata:Detail:SessionResult.credential and success
                                    or #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.last_credential
                                        or #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.last_slave
                                            or #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.__preserved_last_credential) as 'DeviceInfo.last_credential',
                                result as 'DiscoveryAccess.result',
                                end_state as 'DiscoveryAccess.end_state',
                                friendlyTime(starttime) as 'DiscoveryAccess.starttime',
                                friendlyTime(endtime) as 'DiscoveryAccess.endtime',
                                #Member:List:List:DiscoveryRun.label as 'DiscoveryRun.label',
                                _last_marker as 'DiscoveryAccess._last_marker',
                                _first_marker as 'DiscoveryAccess._first_marker',
                                _last_interesting as 'DiscoveryAccess._last_interesting',
                                __had_inference as 'DiscoveryAccess.__had_inference',
                                best_ip_score as 'DiscoveryAccess.best_ip_score',
                                (#DiscoveryAccess:Metadata:Detail:SessionResult.success or access_success) as 'DiscoveryAccess.access_success',
                                access_failure as 'DiscoveryAccess.access_failure',
                                message as 'DiscoveryAccess.message',
                                (#DiscoveryAccess:Metadata:Detail:SessionResult.session_type
                                    or #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.access_method
                                        or #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.last_access_method) as 'DiscoveryAccess.access_method',
                                (kind(#Associate:Inference:InferredElement:)
                                    or inferred_kind
                                        or #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.kind) as 'DiscoveryAccess.inferred_node',
                                #::InferredElement:.__all_ip_addrs as 'InferredElement.__all_ip_addrs',
                                #::InferredElement:.#DeviceWithInterface:DeviceInterface:InterfaceOfDevice:NetworkInterface.ip_addr as 'NetworkInterface.ip_addr'
                            """
                }
device_ids = """
search DiscoveryAccess
show
#::InferredElement:.name as 'InferredElement.name',
#::InferredElement:.hostname as 'InferredElement.hostname',
#::InferredElement:.local_fqdn as 'InferredElement.local_fqdn',
#::InferredElement:.sysname as 'InferredElement.sysname',
endpoint as 'DiscoveryAccess.endpoint',
#DiscoveryAccess:Endpoint:Endpoint:Endpoint.endpoint as 'Endpoint.endpoint',
#DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DiscoveredIPAddressList.#List:List:Member:DiscoveredIPAddress.ip_addr as 'DiscoveredIPAddress.ip_addr',
#::InferredElement:.__all_ip_addrs as 'InferredElement.__all_ip_addrs',
#::InferredElement:.#DeviceWithInterface:DeviceInterface:InterfaceOfDevice:NetworkInterface.ip_addr as 'NetworkInterface.ip_addr',
#::InferredElement:.#DeviceWithInterface:DeviceInterface:InterfaceOfDevice:NetworkInterface.fqdns as 'NetworkInterface.fqdns'
process with unique()
"""
excludes = {"query": """search in '_System' ExcludeRange
                            show
                            exrange_id as 'ID',
                            name as 'Label',
                            range_strings as 'Scan_Range',
                            recurrenceDescription(schedule) as 'Date_Rules'"""}
scanrange = {
                "query":
                """
                search ScanRange where scan_type = 'Scheduled'
                show
                range_id as 'ID',
                label as 'Label',
                (range_strings or provider) as 'Scan_Range',
                scan_level as 'Level',
                recurrenceDescription(schedule) as 'Date_Rules'
                """
               }
last_disco = {
            "query":"""
                    search DiscoveryAccess where endtime
                    ORDER BY discovery_endtime DESC
                    show
                    #id as "DiscoveryAccess.id",
                    #Next:Sequential:Previous:DiscoveryAccess.#id as "DiscoveryAccess.previous_id",
                    #Previous:Sequential:Next:DiscoveryAccess.#id as "DiscoveryAccess.next_id",
                    endpoint as 'DiscoveryAccess.endpoint',
                    #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.hostname as 'DeviceInfo.hostname',
                    #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.os_type as 'DeviceInfo.os_type',
                    #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.os_class as 'DeviceInfo.os_class',
                    #Member:List:List:DiscoveryRun.label as 'DiscoveryRun.label',
                    friendlyTime(#Member:List:List:DiscoveryRun.starttime) as 'DiscoveryRun.starttime',
                    friendlyTime(#Member:List:List:DiscoveryRun.endtime) as 'DiscoveryRun.endtime',
                    friendlyTime(discovery_starttime) as 'DiscoveryAccess.scan_starttime',
                    friendlyTime(discovery_endtime) as 'DiscoveryAccess.scan_endtime',
                    discovery_endtime as 'DiscoveryAccess.scan_endtime_raw',
                    discovery_endtime as 'DiscoveryAccess.discovery_endtime',
                    whenWasThat(discovery_endtime) as 'DiscoveryAccess.when_last_scan',
                    (#DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.last_access_method in ['windows', 'rcmd']
                        and #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.last_slave
                            or #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.probed_os and 'Probe'
                                or #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.last_access_method) as 'DiscoveryAccess.current_access',
                    #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.os_version as 'DeviceInfo.os_version',
                    (nodecount(traverse DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo
                        traverse flags(include_destroyed) Primary:Inference:InferredElement: where not destroyed(#)) > 0) as 'DiscoveryAccess.host_node_updated',
                    end_state as 'DiscoveryAccess.end_state',
                    #Next:Sequential:Previous:DiscoveryAccess.end_state as "DiscoveryAccess.previous_end_state",
                    reason as 'DiscoveryAccess.reason_not_updated',
                    (nodecount(traverse DiscoveryAccess:Metadata:Detail:SessionResult where not provider) > 0) as 'DiscoveryAccess.session_results_logged',
                    (kind(#Associate:Inference:InferredElement:)
                        or inferred_kind
                            or #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.kind) as 'DiscoveryAccess.node_kind',
                    (#DiscoveryAccess:Metadata:Detail:SessionResult.credential and success
                                    or #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.last_credential
                                        or #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.last_slave
                                            or #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.__preserved_last_credential) as 'DeviceInfo.last_credential',
                    result as 'DiscoveryAccess.result',
                    _last_marker as 'DiscoveryAccess._last_marker',
                    _first_marker as 'DiscoveryAccess._first_marker',
                    _last_interesting as 'DiscoveryAccess._last_interesting',
                    __had_inference as 'DiscoveryAccess.__had_inference',
                    best_ip_score as 'DiscoveryAccess.best_ip_score',
                    (#DiscoveryAccess:Metadata:Detail:SessionResult.success or access_success) as 'DiscoveryAccess.access_success',
                    access_failure as 'DiscoveryAccess.access_failure',
                    message as 'DiscoveryAccess.message',
                    (#DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.access_method
                        or #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.last_access_method
                            or #DiscoveryAccess:Metadata:Detail:SessionResult.session_type) as 'DiscoveryAccess.access_method',
                    #::InferredElement:__all_ip_addrs as 'InferredElement.__all_ip_addrs',
                    #::InferredElement:.#DeviceWithInterface:DeviceInterface:InterfaceOfDevice:NetworkInterface.ip_addr as 'NetworkInterface.ip_addr'
                    process with unique()
"""
}

last_disco_basic = {
            "query": """ 
                    search DiscoveryAccess where endtime
                    ORDER BY discovery_endtime DESC
                    show
                    #id as 'DiscoveryAccess.id',
                    endpoint as 'DiscoveryAccess.endpoint',
                    #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.hostname as 'DeviceInfo.hostname',
                    discovery_endtime as 'DiscoveryAccess.discovery_endtime'
                    process with unique()
            """
}

# Simplified "last_disco" retrieval using multiple smaller queries.  The
# ``last_disco`` query above pulls together information across a large number of
# node types which can be expensive to execute.  The following queries break the
# data gathering into individual tables that can be stitched together client
# side using :mod:`pandas`.

# 0) Functional Key extraction used for joins
#
# ``last_disco_functional_key`` is retained for backwards compatibility but the
# reporting code now favours the more granular ``last_disco_key_*`` queries
# defined below.  Each key query maps ``DiscoveryAccess.id`` to a specific
# related node allowing partial lookups when some queries fail.
last_disco_functional_key = {
    "query": """
            search DiscoveryAccess where endtime
            show
            #id as "DiscoveryAccess.id",
            #Next:Sequential:Previous:DiscoveryAccess.#id as "DiscoveryAccess.previous_id",
            #Previous:Sequential:Next:DiscoveryAccess.#id as "DiscoveryAccess.next_id",
            #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.#id as "DeviceInfo.id",
            #Member:List:List:DiscoveryRun.#id as "DiscoveryRun.id",
            #::InferredElement:.#id as "InferredElement.id",
            #DiscoveryAccess:Metadata:Detail:SessionResult.#id as "SessionResult.id",
            explode #::InferredElement:.#DeviceWithInterface:DeviceInterface:InterfaceOfDevice:NetworkInterface.#id as "NetworkInterface.id"
            processwith unique()
            """,
}

# 0a) DiscoveryAccess -> DeviceInfo key mapping
last_disco_key_deviceinfo = {
    "query": """
            search DiscoveryAccess where endtime
            show
            #id as "DiscoveryAccess.id",
            #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.#id as "DeviceInfo.id"
            processwith unique()
            """,
}

# 0b) DiscoveryAccess -> DiscoveryRun key mapping
last_disco_key_run = {
    "query": """
            search DiscoveryAccess where endtime
            show
            #id as "DiscoveryAccess.id",
            #Member:List:List:DiscoveryRun.#id as "DiscoveryRun.id"
            processwith unique()
            """,
}

# 0c) DiscoveryAccess -> InferredElement key mapping
last_disco_key_inferred = {
    "query": """
            search DiscoveryAccess where endtime
            show
            #id as "DiscoveryAccess.id",
            #::InferredElement:.#id as "InferredElement.id"
            processwith unique()
            """,
}

# 0d) DiscoveryAccess -> SessionResult key mapping
last_disco_key_session = {
    "query": """
            search DiscoveryAccess where endtime
            show
            #id as "DiscoveryAccess.id",
            explode #DiscoveryAccess:Metadata:Detail:SessionResult.#id as "SessionResult.id"
            processwith unique()
            """,
}

# 0e) DiscoveryAccess -> NetworkInterface key mapping
last_disco_key_interface = {
    "query": """
            search DiscoveryAccess where endtime
            show
            #id as "DiscoveryAccess.id",
            explode #::InferredElement:.#DeviceWithInterface:DeviceInterface:InterfaceOfDevice:NetworkInterface.#id as "NetworkInterface.id"
            processwith unique()
            """,
}

# A) DiscoveryAccess — all core facts
last_disco_access = {
    "query": """
            search DiscoveryAccess where endtime
            ORDER BY discovery_endtime DESC
            show
            #id as "DiscoveryAccess.id",
            #Next:Sequential:Previous:DiscoveryAccess.#id as "DiscoveryAccess.previous_id",
            #Previous:Sequential:Next:DiscoveryAccess.#id as "DiscoveryAccess.next_id",
            endpoint as 'DiscoveryAccess.endpoint',
            friendlyTime(discovery_starttime) as 'DiscoveryAccess.scan_starttime',
            friendlyTime(discovery_endtime) as 'DiscoveryAccess.scan_endtime',
            discovery_endtime as 'DiscoveryAccess.scan_endtime_raw',
            discovery_endtime as 'DiscoveryAccess.discovery_endtime',
            whenWasThat(discovery_endtime) as 'DiscoveryAccess.when_last_scan',
            end_state as 'DiscoveryAccess.end_state',
            reason as 'DiscoveryAccess.reason_not_updated',
            result as 'DiscoveryAccess.result',
            _last_marker as 'DiscoveryAccess._last_marker',
            _first_marker as 'DiscoveryAccess._first_marker',
            _last_interesting as 'DiscoveryAccess._last_interesting',
            __had_inference as 'DiscoveryAccess.__had_inference',
            best_ip_score as 'DiscoveryAccess.best_ip_score',
            (#DiscoveryAccess:Metadata:Detail:SessionResult.success or access_success) as 'DiscoveryAccess.access_success',
            access_failure as 'DiscoveryAccess.access_failure',
            message as 'DiscoveryAccess.message'
            process with unique()
            """,
}

# B) DeviceInfo — OS/identity/credential fields
last_disco_deviceinfo = {
    "query": """
            search DeviceInfo
            show
            #id as "DeviceInfo.id",
            hostname as 'DeviceInfo.hostname',
            os_type as 'DeviceInfo.os_type',
            os_class as 'DeviceInfo.os_class',
            os_version as 'DeviceInfo.os_version',
            kind as 'DeviceInfo.kind',
            inferred_kind as 'DeviceInfo.inferred_kind',
            last_access_method as 'DeviceInfo.last_access_method',
            probed_os as 'DeviceInfo.probed_os',
            last_credential as 'DeviceInfo.last_credential',
            last_slave as 'DeviceInfo.last_slave',
            __preserved_last_credential as 'DeviceInfo.__preserved_last_credential'
            process with unique()
            """,
}

# C) DiscoveryRun — labels & times
last_disco_run = {
    "query": """
            search DiscoveryRun
            show
            #id as "DiscoveryRun.id",
            label as 'DiscoveryRun.label',
            friendlyTime(starttime) as 'DiscoveryRun.starttime',
            friendlyTime(endtime) as 'DiscoveryRun.endtime'
            process with unique()
            """,
}

# D) SessionResult — success/type/provider
last_disco_session = {
    "query": """
            search SessionResult
            show
            #id as "SessionResult.id",
            success as "SessionResult.success",
            session_type as "SessionResult.session_type",
            provider as "SessionResult.provider"
            process with unique()
            """,
}

# E) InferredElement — IP aggregates
last_disco_inferred = {
    "query": """
            search InferredElement
            show
            #id as "InferredElement.id",
            __all_ip_addrs as 'InferredElement.__all_ip_addrs'
            process with unique()
            """,
}

# F) NetworkInterface — per-interface IPs
last_disco_interface = {
    "query": """
            search NetworkInterface
            show
            #id as "NetworkInterface.id",
            ip_addr as 'NetworkInterface.ip_addr'
            process with unique()
            """,
}
ip_schedules = """search DiscoveryAccess
                    show endpoint,
                    nodecount(traverse Member:List:List:DiscoveryRun where scan_type = 'Scheduled') as 'schedules'
                    process with unique()"""

active_scans = """
                    search DiscoveryRun where not endtime
                    show run_id as 'DiscoveryRun.run_id',
                         status as 'DiscoveryRun.status',
                         range_id as 'DiscoveryRun.range_id',
                         total as 'DiscoveryRun.total',
                         scanning as 'DiscoveryRun.scanning',
                         pre_scanning as 'DiscoveryRun.pre_scanning',
                         done as 'DiscoveryRun.done'
                """

connections_unscanned = """
                    search Host
                    traverse InferredElement:Inference:Associate:DiscoveryAccess
                    traverse DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:NetworkConnectionList
                    traverse List:List:Member:DiscoveredNetworkConnection
                    order by remote_ip_addr
                    show
                    remote_ip_addr as 'Unscanned Host IP Address'
                    processwith connectionsToUnseen
                    """

dropped_endpoints = """
                    search DroppedEndpoints
                    show explode endpoints as 'Endpoint',
                    reason as 'Reason_Not_Updated',
                    __reason as 'End_State',
                    friendlyTime(starttime) as 'Start',
                    friendlyTime(endtime) as 'End',
                    endtime as 'End_Raw',
                    whenWasThat(endtime) as 'When_Last_Scan',
                    #EndpointRange:EndpointRange:DiscoveryRun:DiscoveryRun.label as "Run"
                """

sensitive_data = """
                        search DiscoveredProcess
                        where ((args has subword 'user' or args has substring 'username')
                            and (args has subword 'pass' or args has substring 'password'))
                        or (args matches regex '(?i)\\s-u(\\s+|=)\\S+'
                            and args matches regex '(?i)\\s-p(\\s+|=)\\S+')
                        show
                        #Member:List:List:ProcessList.#DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.#DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.hostname as 'Host',
                        #Member:List:List:ProcessList.#DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.endpoint as 'Endpoint',
                        username,
                        cmd,
                        args,
                        (extract(args, regex '(?i)(user(name)?.*?\\S+)', raw '\\1')
                            or extract(args, regex '(?i)(-u.*?\\S+)', raw '\\1')) as 'Matched Username String',
                        extract(args, regex '(?i)(password.*?\\S+|\\s-p.*?\\S+)', raw '\\1') as 'Matched Password String'
                    """

tpl_export = """
                    search KnowledgeUpload
                    where not origin = 'TKU'
                    traverse Upload:UploadContents:UploadItem:PatternModule
                    show
                    name,
                    content
                """

eca_error = """
                    search ECAError
                    show
                    summary,
                    action_name,
                    rule_name,
                    traceback,
                    #:::DiscoveryAccess.starttime as 'Discovery Start Time'
               """

scan_ranges = """
                    search ScanRange
                    where not scan_type = 'Snapshot'
                    show
                    label as 'Label',
                    range_strings as 'IP Range',
                    scan_level as 'Level',
                    recurrenceDescription(schedule) as 'Date Rules',
                    created_by as 'User',
                    created_time as 'Created',
                    enabled as 'enabled'
                 """

exclude_ranges = """
                        search in '_System' ExcludeRange
                        show
                        name as 'Label',
                        range_strings as 'Range',
                        recurrenceDescription(schedule) as 'Date Rules',
                        description as 'Description',
                        fullFoundationName(created_by) as 'User'
                    """

id_change = """
                    search flags(find_relationships) EndpointIdentity
                    order by endpoint, creationTime(#) desc
                    show
                    time(creationTime(#)) as 'Identity Change Time',
                    endpoint as 'Endpoint',
                    kind(#:Previous:.#) as 'Previous Kind',
                    nodeLink(#:Previous:.#InferredElement:Inference:Primary:DeviceInfo.#DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.#, time(#:Previous:.#InferredElement:Inference:Primary:DeviceInfo.#DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.starttime)) as 'Last Update of Previous Identity',
                    nodeLink(#:Previous:.#, #:Previous:.name) as 'Previous Identity',
                    nodeLink(#:Next:.#, #:Next:.name) as 'Next Identity',
                    nodeLink(#:Next:.#InferredElement:Inference:Primary:DeviceInfo.#DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.#, time(#:Next:.#InferredElement:Inference:Primary:DeviceInfo.#DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.starttime)) as 'Last Update of Next Identity',
                    kind(#:Next:.#) as 'Next Kind'
               """

open_ports = """
                    search DiscoveredListeningPort
                    with
                    ((local_port  = 161) and 'SNMP'
                    or (local_port  = 21) and 'FTP'
                    or (local_port  = 22) and 'SSH'
                    or (local_port  = 23) and 'Telnet'
                    or (local_port  = 25) and 'SMTP'
                    or (local_port  = 53) and 'DNS'
                    or (local_port  = 69) and 'TFTP'
                    or (local_port  = 110) and 'POP3'
                    or (local_port  = 119) and 'NNTP'
                    or (local_port  = 137) and 'NetBios'
                    or (local_port  = 143) and 'IMAP'
                    or (local_port  and 'other')) as openports
                    where @openports not in 'other'
                    show
                    #Member:List:List:NetworkConnectionList.#DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.#DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:HostInfo.#Primary:Inference:InferredElement:Host.name as 'hostname',
                    #Member:List:List:NetworkConnectionList.#DiscoveryResult:DiscoveryAccessResult:DiscoveryAccess:DiscoveryAccess.endpoint as 'endpoint',
                    @openports as 'Default Service Port Open'
                    process with countUnique(0)
                """
host_utilisation = """
                        search Host where type <> 'Hypervisor'
                        show
                        hostname as 'Host.hostname',
                        hash(hostname) as 'Host.hostname_hash',
                        os as 'Host.os',
                        os_type as 'Host.os_type',
                        virtual as 'Host.virtual',
                        cloud as 'Host.cloud',
                        #InferredElement:Inference:Associate:DiscoveryAccess.endpoint as 'DiscoveryAccess.endpoint',
                        nodecount(traverse :::SoftwareInstance) as 'Host.running_software_instances',
                        nodecount(traverse :::CandidateSoftwareInstance) as 'Host.candidate_software_instances',
                        nodecount(traverse :::DiscoveryAccess where _last_marker traverse :::ProcessList traverse :::DiscoveredProcess) as 'Host.running_processes',
                        nodecount(traverse :::DiscoveryAccess where _last_marker traverse :::ServiceList traverse :::DiscoveredService where state = 'RUNNING') as 'Host.running_services'
                      """

orphan_vms = """
                    search Host
                    where virtual
                    and nodecount(traverse ContainedHost:HostContainment:HostContainer:VirtualMachine) = 0
                    order by name
                    show
                    hostname,
                    hash(hostname) as 'hashed_hostname',
                    os,
                    #InferredElement:Inference:Associate:DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.os_type as 'OS_Type',
                    virtual,
                    cloud,
                    #InferredElement:Inference:Associate:DiscoveryAccess.endpoint as 'endpoint',
                    vendor,
                    vm_class
                """

audit = r"""
            search in 'Audit' UserEventAuditRecord
            where not (user matches '^\[\w+\]$')
            show
            event,
            event_group,
            user,
            when,
            msg,
            ip_addr as 'Ip Addr'
           """

near_removal = """
                    search flags(no_segment) Host, StorageSystem, Printer
                    with value(getOption('MIN_FAILED_ACCESSES_BEFORE_DESTROY') + age_count) as scans,
                    value(abs(last_update_success) / 10000000) as lus,
                    value(currentTime() / 10000000 - getOption('MIN_SECONDS_SINCE_ACCESS_SUCCESS_BEFORE_DESTROY') + 2 * 24 * 3600) as time_threshold,
                    value((getOption('MIN_SECONDS_SINCE_ACCESS_SUCCESS_BEFORE_DESTROY') + abs(last_update_success) / 10000000 - currentTime() / 10000000) / 3600) as time_to_doom
                    where @scans < 3
                    show
                    kind(#) as 'CI Type',
                    type as 'Product/Class',
                    name as 'Name',
                    hash(name) as 'Hashed Name',
                    (os_type or instance) as 'Instance',
                    (#InferredElement:Inference:Associate:DiscoveryAccess.endpoint or 'DDD Aged Out') as 'Last Successful IP',
                    whenWasThat(last_update_success) as 'Last Successful Scan',
                    last_update_success as 'Last Successful Scan Date',
                    value(age_count * -1) as 'Consecutive Scan Failures',
                    (@scans > 0 and @time_to_doom > 0 and #'%d scans, %d hours'(@scans,@time_to_doom)
                    or @scans > 0 and #'%d scans'(@scans) or @time_to_doom > 0 and #'%d hours'(@time_to_doom)
                    or 'Next unsuccessful scan') as 'Removal Eligibility'
                  """

removed = """
                search flags(include_destroyed, exclude_current, no_segment) Host, Printer, StorageSystem
                with kind(#Previous:::.#) as pk,
                value(#Previous:EndpointIdentity:Next:.name) as ph,
                kind(#Next:::.#) as nk,
                value(#Next:EndpointIdentity:Previous:.name) as nh
                where not type matches 'Windows Desktop'
                and destructionTime(#) > (currentTime() - 7*24*3600*10000000)
                show
                kind(#) as 'kind',
                name as 'name',
                hash(name) as 'hashed_name',
                os as 'os',
                unique((#InferredElement:Inference:Associate:DiscoveryAccess.endpoint or 'DDD Aged Out')) as 'Last Successful IP',
                whenWasThat(last_update_success) as 'Last Successful Scan',
                fmt('%s (%s)', @ph, @pk) as 'Previous Found',
                fmt('%s (%s)', @nh, @nk) as 'Next Found',
                @nk as 'next kind', @pk as 'prv kind',
                time(destructionTime(#)) as 'Destroyed When'
             """

os_lifecycle = """
                    search Host
                    where #ElementWithDetail:SupportDetail:OSDetail:SupportDetail.retirement_date
                        or #ElementWithDetail:SupportDetail:OSDetail:SupportDetail.end_support_date
                            or #ElementWithDetail:SupportDetail:OSDetail:SupportDetail.end_ext_support_date
                    show
                    name,
                    (#ElementWithDetail:SupportDetail:OSDetail:SupportDetail.retirement_date
                        and formatTime(#ElementWithDetail:SupportDetail:OSDetail:SupportDetail.retirement_date, '%Y-%m-%d')) as 'End of Life',
                    (#ElementWithDetail:SupportDetail:OSDetail:SupportDetail.end_support_date
                        and formatTime(#ElementWithDetail:SupportDetail:OSDetail:SupportDetail.end_support_date, '%Y-%m-%d')) as 'End of Support',
                    (#ElementWithDetail:SupportDetail:OSDetail:SupportDetail.end_ext_support_date
                        and formatTime(#ElementWithDetail:SupportDetail:OSDetail:SupportDetail.end_ext_support_date, '%Y-%m-%d')) as 'End of Ext Support',
                    (#ElementWithDetail:SupportDetail:OSDetail:SupportDetail.end_ext_support_date
                        and (#ElementWithDetail:SupportDetail:OSDetail:SupportDetail.end_ext_support_date < currentTime()
                        and 'EOES Exceeded')
                        or #ElementWithDetail:SupportDetail:OSDetail:SupportDetail.end_support_date
                            and (#ElementWithDetail:SupportDetail:OSDetail:SupportDetail.end_support_date < currentTime()
                            and 'EOS Exceeded') or #ElementWithDetail:SupportDetail:OSDetail:SupportDetail.retirement_date
                            and (#ElementWithDetail:SupportDetail:OSDetail:SupportDetail.retirement_date < currentTime()
                            and 'EOL Exceeded')
                            or (#ElementWithDetail:SupportDetail:OSDetail:SupportDetail.retirement_date
                                and (#ElementWithDetail:SupportDetail:OSDetail:SupportDetail.retirement_date < currentTime() + 182 * 864000000000
                                and 'EOL less than 6 months away')
                                or #ElementWithDetail:SupportDetail:OSDetail:SupportDetail.end_support_date
                                    and (#ElementWithDetail:SupportDetail:OSDetail:SupportDetail.end_support_date < currentTime() + 182 * 864000000000
                                    and 'EOS less than 6 months away')
                                    or #ElementWithDetail:SupportDetail:OSDetail:SupportDetail.end_ext_support_date
                                        and (#ElementWithDetail:SupportDetail:OSDetail:SupportDetail.end_ext_support_date < currentTime() + 182 * 864000000000
                                        and 'EOES less than 6 months away'))
                                        or (#ElementWithDetail:SupportDetail:OSDetail:SupportDetail.retirement_date
                                            and 'EOL more than 6 months away'
                                            or #ElementWithDetail:SupportDetail:OSDetail:SupportDetail.end_support_date
                                                and 'EOS more than 6 months away'
                                                or #ElementWithDetail:SupportDetail:OSDetail:SupportDetail.end_ext_support_date
                                                    and 'EOES more than 6 months away')) as 'Lifecycle Risk',
                    taxonomy 'summary_no_name'
                  """

software_lifecycle = """
                            search SoftwareInstance
                            where
                            #ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.retirement_date
                                or #ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_support_date
                                    or #ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_ext_support_date
                            show
                            type,
                            product_version,
                            (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.retirement_date
                                and formatTime(#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.retirement_date, '%Y-%m-%d')) as 'End of Life',
                            (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_support_date
                                and formatTime(#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_support_date, '%Y-%m-%d')) as 'End of Support',
                            (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_ext_support_date
                                and formatTime(#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_ext_support_date, '%Y-%m-%d')) as 'End of Ext Support',
                            (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_ext_support_date
                                and (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_ext_support_date < currentTime()
                                and 'EOES Exceeded')
                                or #ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_support_date
                                    and (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_support_date < currentTime()
                                    and 'EOS Exceeded')
                                    or #ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.retirement_date
                                        and (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.retirement_date < currentTime()
                                        and 'EOL Exceeded')
                                        or (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.retirement_date
                                            and (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.retirement_date < currentTime() + 182 * 864000000000
                                            and 'EOL less than 6 months away')
                                            or #ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_support_date
                                                and (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_support_date < currentTime() + 182 * 864000000000
                                                and 'EOS less than 6 months away')
                                                or #ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_ext_support_date
                                                    and (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_ext_support_date < currentTime() + 182 * 864000000000
                                                    and 'EOES less than 6 months away'))
                                                    or (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.retirement_date
                                                        and 'EOL more than 6 months away'
                                                        or #ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_support_date
                                                            and 'EOS more than 6 months away'
                                                            or #ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_ext_support_date
                                                                and 'EOES more than 6 months away')) as 'Lifecycle Risk',
                            #:HostedSoftware:Host:Host.name as 'Host'
                        """

db_lifecycle = """
                    search Pattern
                    where
                    'Relational Database Management Systems' in categories
                    traverse Pattern:Maintainer:Element:SoftwareInstance
                        where #ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.retirement_date
                            or #ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_support_date
                                or #ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_ext_support_date
                    show
                    type,
                    product_version,
                    (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.retirement_date
                        and formatTime(#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.retirement_date, '%Y-%m-%d')) as 'End of Life',
                    (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_support_date
                        and formatTime(#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_support_date, '%Y-%m-%d')) as 'End of Support',
                    (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_ext_support_date
                        and formatTime(#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_ext_support_date, '%Y-%m-%d')) as 'End of Ext Support',
                    (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_ext_support_date
                        and (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_ext_support_date < currentTime()
                        and 'EOES Exceeded')
                        or #ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_support_date
                            and (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_support_date < currentTime()
                            and 'EOS Exceeded')
                            or #ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.retirement_date
                                and (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.retirement_date < currentTime()
                                and 'EOL Exceeded')
                                or (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.retirement_date
                                    and (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.retirement_date < currentTime() + 182 * 864000000000
                                    and 'EOL less than 6 months away')
                                    or #ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_support_date
                                        and (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_support_date < currentTime() + 182 * 864000000000
                                        and 'EOS less than 6 months away')
                                        or #ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_ext_support_date
                                            and (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_ext_support_date < currentTime() + 182 * 864000000000
                                            and 'EOES less than 6 months away'))
                                            or (#ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.retirement_date
                                                and 'EOL more than 6 months away'
                                                or #ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_support_date
                                                    and 'EOS more than 6 months away'
                                                    or #ElementWithDetail:SupportDetail:SoftwareDetail:SupportDetail.end_ext_support_date
                                                        and 'EOES more than 6 months away')) as 'Lifecycle Risk',
                    #:HostedSoftware:Host:Host.name as 'Host'
                """

licenses = """
                search Host
                where not (host_type has subword 'desktop' or host_type has subword 'client')
                show
                versionInfo() as 'BMC Discovery Version',
                (local_fqdn or name) as 'Name',
                hash((local_fqdn or name)) as 'Anonymized Name',
                os as 'Discovered OS'
                processwith unique(0)
             """

snmp_devices = """
                    search DiscoveryAccess where
                    _last_marker defined
                    and endtime defined
                    and end_state = 'UnsupportedDevice'
                    and nodecount(traverse flags(include_destroyed) ::InferredElement:Host) = 0
                    and #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.kind <> 'Host'
                    and nodecount (traverse DiscoveryAccess:Metadata:Detail:SessionResult where session_type has subword "SNMP" and success) > 0
                    show
                    #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.os_class as 'OS_Class',
                    #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.sysobjectid as 'SNMP_sysObjectId',
                    (#DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.probed_os and 'Probe' or #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.access_method) as 'Current_Access',
                    #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.os as 'Discovered_OS',
                    #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.os_type as 'OS_Type',
                    #DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo.os_version as 'OS_Version'
                    process with countUnique()
                  """

capture_candidates = """
                    search DiscoveryAccess where end_state = 'UnsupportedDevice' and _last_marker
                    traverse DiscoveryAccess:DiscoveryAccessResult:DiscoveryResult:DeviceInfo where sysobjectid
                    show
                    access_method as 'Access Method',
                    request_time as 'Request Time',
                    hostname as 'Hostname',
                    os as 'OS',
                    failure_reason as 'Failure Reason',
                    syscontact as 'Syscontact',
                    syslocation as 'Syslocation',
                    sysdescr as 'Sysdescr',
                    sysobjectid as 'Sysobject ID'
                """

missing_vms = """
                    search VirtualMachine
                    where nodecount(traverse HostContainer:HostContainment:ContainedHost:) = 0
                    show
                    vm_type as 'VirtualMachine.vm_type',
                    (product_version or cloud_class) as 'VirtualMachine.product_version',
                    #RunningSoftware:HostedSoftware:Host:.name as 'Host.name',
                    #RunningSoftware:HostedSoftware:Host:.type as 'Host.type',
                    vm_name as 'VirtualMachine.vm_name',
                    vm_guest_os as 'VirtualMachine.vm_guest_os',
                    guest_full_name as 'VirtualMachine.guest_full_name',
                    (vm_status or cloud and "Cloud Hosted") as 'VirtualMachine.vm_status'
                """

agents = """
                search Host
                with
                nodecount(traverse Host:HostedSoftware::SoftwareInstance where type = 'Microsoft System Center Configuration Manager Client') as SCCM,
                nodecount(traverse Host:HostedSoftware::SoftwareInstance where type = 'Sophos Anti-Virus') as SophosAV,
                nodecount(traverse Host:HostedSoftware::SoftwareInstance where type = 'Qualys Cloud Agent') as QualysCloud,
                nodecount(traverse Host:HostedSoftware::SoftwareInstance where type = 'BMC Client Management Client') as BCM,
                nodecount(traverse Host:HostedSoftware::SoftwareInstance where type = 'McAfee Endpoint Security') as McAfee,
                nodecount(traverse Host:HostedSoftware::SoftwareInstance where type = 'BMC Patrol Agent') as Patrol,
                nodecount(traverse Host:HostedSoftware::SoftwareInstance where type = 'Symantec Endpoint Protection Client') as Symantec
                where os_type has subword 'Windows'
                show
                name as 'Host.name',
                hash(name) as 'Host.hashed_name',
                os_version as 'Host.os_version',
                #HostedSoftware:RunningSoftware:SoftwareInstance.name as 'SoftwareInstance.name',
                serial as 'Host.serial',
                uuid as 'Host.uuid',
                ((age_count < 0) and 'Aging' or 'Alive') as 'Host.age_status',
                whenWasThat(last_update_success) as 'Host.last_successful_scan',
                last_update_success as 'Host.last_scan_date',
                (@SCCM and 'Yes' or '-') as 'Host.sccm',
                (@SophosAV and 'Yes' or '-') as 'Host.sophos_av',
                (@QualysCloud and 'Yes' or '-') as 'Host.qualys_agent',
                (@BCM and 'Yes' or '-') as 'Host.bcm',
                (@McAfee and 'Yes' or '-') as 'Host.mcafee',
                (@Patrol and 'Yes' or '-') as 'Host.patrol',
                (@Symantec and 'Yes' or '-') as 'Host.symantec'
            """

user_accounts = """
                        search SoftwareInstance
                        show
                        name as "Software_Instance",
                        #RunningSoftware:HostedSoftware:Host:.name as 'Host',
                        type as 'Type',
                        product_version as 'Version',
                        explode #InferredElement:Inference:Primary:DiscoveredProcess.username as 'User_Name'
                   """

cmdb_sync_config = """
                        SEARCH IN '_System' CMDBSyncConfig
                   """

patterns =    """
                    search PatternModule
                    show origin as 'Origin',
                    tree_path as 'Tree_Path',
                    name,
                    submitting_user,
                    submission_date as 'Submission_Date',
                    active as 'Active',
                    description as 'Description',
                    extra_node_kinds as 'Extra_Node_Kinds',
                    extra_rel_kinds as 'Extra_Rel_Kinds'
                """

discovery_run_analysis = """
                    search DiscoveryRun as DiscoveryRun
                      with (traverse :::ScanRange as ScanRange),
                           (traverse :::DroppedEndpoints as DroppedEndpoints),
                           (traverse :::DiscoveryAccess as DiscoveryAccess)
                      show valid_ranges as 'Explicit Ranges', label as 'Scan Label',
                           range_summary as 'Range Summary', outpost_name as 'Outpost Name',
                           #ScanRange.label as 'Label', #ScanRange.scan_kind as 'Scan Kind',
                           (#ScanRange.range_strings or #ScanRange.provider) as 'Range',
                           recurrenceDescription(#ScanRange.schedule) as 'Schedule',
                           total as 'Total Endpoints',
                           (result_success or 0) + (result_skipped or 0) + (result_error or 0) +
                           (result_no_access or 0) + (result_no_response or 0) as 'Active Endpoints',
                           (result_dropped or 0) as 'Dropped',
                           unique(#DiscoveryAccess.scan_kind) as 'Scan Kinds'
                      processwith show valid_ranges, label, endtime as 'End Time',
                           range_summary, outpost_name, @4, @5, @6, @7, total, @9, @10,
                           @11 as 'Scan Kinds'
                """
