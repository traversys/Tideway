import csv
import json
from types import SimpleNamespace

from tideway.dismal import api, defaults


class FakeResponse:
    ok = True
    status_code = 200
    reason = "OK"
    url = "https://appliance/api/v1.14/knowledge"

    def __init__(self, data):
        self._data = data
        self.text = json.dumps(data)

    def json(self):
        return self._data


class FakeKnowledge:
    def __init__(self, data):
        self.response = FakeResponse(data)

    @property
    def get_knowledge(self):
        return self.response


def test_tku_handles_null_optional_modules(tmp_path):
    knowledge = FakeKnowledge(
        {
            "latest_tku": {"name": "TKU-2025-06-1"},
            "latest_edp": None,
            "latest_storage": None,
            "latest_servicenow_sync": None,
        }
    )
    args = SimpleNamespace(
        target="192.0.2.10",
        output_file=None,
        output_csv=False,
        output_null=False,
        output_cli=False,
        excavate=["tku"],
        preserve_existing=False,
    )

    api.tku(knowledge, args, str(tmp_path))

    with (tmp_path / defaults.tku_filename).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))

    assert rows == [
        ["Discovery Instance", "TKU"],
        ["192.0.2.10", "TKU-2025-06-1"],
        ["192.0.2.10", "Not installed"],
        ["192.0.2.10", "Not installed"],
    ]
