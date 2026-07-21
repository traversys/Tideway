from tideway.dismal import queries, reporting


def test_chunked_last_disco_uses_scalar_granular_keys(monkeypatch):
    responses = {
        id(queries.last_disco_key_deviceinfo): [
            {"DiscoveryAccess.id": "access-1", "DeviceInfo.id": "device-1"}
        ],
        id(queries.last_disco_key_run): [
            {"DiscoveryAccess.id": "access-1", "DiscoveryRun.id": "run-1"}
        ],
        id(queries.last_disco_key_inferred): [
            {"DiscoveryAccess.id": "access-1", "InferredElement.id": "host-1"}
        ],
        id(queries.last_disco_key_session): [
            {"DiscoveryAccess.id": "access-1", "SessionResult.id": "session-1"}
        ],
        id(queries.last_disco_key_interface): [
            {"DiscoveryAccess.id": "access-1", "NetworkInterface.id": "interface-1"}
        ],
        id(queries.last_disco_access): [
            {
                "DiscoveryAccess.id": "access-1",
                "DiscoveryAccess.previous_id": None,
                "DiscoveryAccess.next_id": None,
                "DiscoveryAccess.end_state": "OK",
            }
        ],
        id(queries.last_disco_deviceinfo): [
            {
                "DeviceInfo.id": "device-1",
                "DeviceInfo.last_access_method": "ssh",
                "DeviceInfo.last_slave": None,
                "DeviceInfo.probed_os": False,
            }
        ],
        id(queries.last_disco_run): [
            {"DiscoveryRun.id": "run-1", "DiscoveryRun.label": "scan"}
        ],
        id(queries.last_disco_session): [
            {
                "SessionResult.id": "session-1",
                "SessionResult.provider": None,
                "SessionResult.session_type": "ssh",
                "SessionResult.success": True,
            }
        ],
        id(queries.last_disco_inferred): [
            {"InferredElement.id": "host-1", "InferredElement.__all_ip_addrs": ["192.0.2.1"]}
        ],
        id(queries.last_disco_interface): [
            {"NetworkInterface.id": "interface-1", "NetworkInterface.ip_addr": "192.0.2.1"}
        ],
    }

    def fake_search_results(_search, query, *args, **kwargs):
        if query is queries.last_disco_functional_key:
            raise AssertionError("legacy list-valued key query must not be used")
        return responses.get(id(query), [])

    monkeypatch.setattr(reporting.api, "search_results", fake_search_results)

    result = reporting.chunked_last_disco(object())

    assert len(result) == 1
    assert result.loc[0, "SessionResult.id"] == "session-1"
    assert result.loc[0, "DiscoveryAccess.access_method"] == "ssh"
