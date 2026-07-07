import tideway
from tideway import notebooks as tw_nb


class DummyResponse:
    def __init__(self, data, ok=True):
        self._data = data
        self.ok = ok

    def json(self):
        return self._data


def test_api_version_from_config_uses_configured_value(monkeypatch):
    def fail_get(*args, **kwargs):
        raise AssertionError("/api/about should not be called for configured versions")

    monkeypatch.setattr(tideway.main.requests, "get", fail_get)

    version = tw_nb.api_version_from_config({"api_version": "v1.13"}, "host", "token")

    assert version == "1.13"


def test_api_version_from_config_detects_highest_supported(monkeypatch):
    def fake_get(url, verify=False):
        assert url == "https://host/api/about"
        return DummyResponse({"api_versions": ["1.2", "1.14", "1.9"]})

    monkeypatch.setattr(tideway.main.requests, "get", fake_get)

    version = tw_nb.api_version_from_config({}, "host", "token")

    assert version == "1.14"


def test_appliance_from_config_detects_api_version(monkeypatch, tmp_path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "appliances:\n"
        "  - name: sandbox\n"
        "    target: host\n"
        "    token: token\n",
        encoding="utf-8",
    )

    def fake_get(url, verify=False):
        assert url == "https://host/api/about"
        return DummyResponse({"api_versions": ["1.0", "1.14"]})

    monkeypatch.setattr(tideway.main.requests, "get", fake_get)

    tw = tw_nb.appliance_from_config(config_path=str(config_path))

    assert tw.api_version == "1.14"
    assert tw.url == "https://host/api/v1.14"
