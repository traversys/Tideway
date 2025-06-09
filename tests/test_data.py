import json
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tideway.data import Data

class DummyResponse:
    def __init__(self, data, ok=True):
        self._data = data
        self.ok = ok
    def json(self):
        return self._data


def test_search_bulk_pagination(monkeypatch):
    responses = []
    initial = [{
        "headings": ["col1"],
        "results": [{"col1": 1}, {"col1": 2}],
        "count": 4,
        "results_id": "rid",
        "next_offset": 2
    }]
    second = [{
        "results": [{"col1": 3}, {"col1": 4}]
    }]
    responses.extend([DummyResponse(initial), DummyResponse(second)])

    def fake_search(self, query, offset=None, results_id=None, format=None, limit=100, delete=False):
        return responses.pop(0)

    monkeypatch.setattr(Data, "search", fake_search)

    d = Data("host", "token")
    result = d.search_bulk("query")
    assert result == [["col1"], {"col1": 1}, {"col1": 2}, {"col1": 3}, {"col1": 4}]
    assert responses == []
