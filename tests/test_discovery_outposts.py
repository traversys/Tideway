import tideway
from tideway.discovery import Discovery

class DummyResponse:
    def __init__(self, data=None):
        self._data = data or {}
    def json(self):
        return self._data


def test_get_discovery_outpost_endpoint(monkeypatch):
    calls = []
    def fake_request(self, endpoint):
        calls.append(endpoint)
        return DummyResponse({"id": "all"})
    monkeypatch.setattr(tideway.discoRequests, "discoRequest", fake_request)

    d = Discovery("host", "token")
    resp = d.get_discovery_outpost()
    assert calls == ["/discovery/outposts"]
    assert resp.json()["id"] == "all"

    calls.clear()
    resp = d.get_discovery_outpost("abc")
    assert calls == ["/discovery/outposts/abc"]


def test_post_discovery_outpost(monkeypatch):
    called = {}
    def fake_post(self, endpoint, body):
        called["endpoint"] = endpoint
        called["body"] = body
        return DummyResponse({"created": True})
    monkeypatch.setattr(tideway.discoRequests, "discoPost", fake_post)

    d = Discovery("host", "token")
    body = {"name": "op"}
    resp = d.post_discovery_outpost(body)
    assert called["endpoint"] == "/discovery/outposts"
    assert called["body"] == body
    assert resp.json()["created"] is True


def test_delete_discovery_outpost(monkeypatch):
    calls = []
    def fake_delete(self, endpoint):
        calls.append(endpoint)
        return DummyResponse({"deleted": True})
    monkeypatch.setattr(tideway.discoRequests, "discoDelete", fake_delete)

    d = Discovery("host", "token")
    resp = d.delete_discovery_outpost("xyz")
    assert calls == ["/discovery/outposts/xyz"]
    assert resp.json()["deleted"] is True
