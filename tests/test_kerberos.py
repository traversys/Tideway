import tideway
from tideway.kerberos import Kerberos

class DummyResponse:
    pass

def test_get_vault_kerberos_realm_calls_once(monkeypatch):
    calls = []
    def fake_request(self, endpoint):
        calls.append(endpoint)
        return DummyResponse()

    monkeypatch.setattr(tideway.discoRequests, "discoRequest", fake_request)

    kb = Kerberos("host", "token")
    kb.get_vault_kerberos_realm()
    assert calls == ["/vault/kerberos/realms"]

    calls.clear()
    kb.get_vault_kerberos_realm("EXAMPLE")
    assert calls == ["/vault/kerberos/realms/EXAMPLE"]
