import tideway
from tideway.main import Appliance

class DummyResponse:
    def __init__(self, data, status_code=200):
        self._data = data
        self.status_code = status_code
        self.ok = status_code < 400
    def json(self):
        return self._data


def test_api_paths_lookup(monkeypatch):
    schema = {"paths": {"/about": {"get": {"summary": "About"}}}}

    def fake_get(url, verify=False):
        return DummyResponse(schema)

    monkeypatch.setattr(tideway.main.requests, "get", fake_get)

    tw = Appliance("host", "token")
    paths = tw.api_paths()
    assert "/about" in paths
    assert tw.api_paths("/about") == {"get": {"summary": "About"}}
    assert tw.api_paths("/missing") is None
