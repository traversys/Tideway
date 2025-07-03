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

    def fake_search_once(self, query, offset=None, results_id=None, format=None, limit=100, delete=False):
        return responses.pop(0)

    monkeypatch.setattr(Data, "_search_once", fake_search_once)

    d = Data("host", "token")
    result = d.search_bulk("query")
    assert result == [["col1"], {"col1": 1}, {"col1": 2}, {"col1": 3}, {"col1": 4}]
    assert responses == []


def test_search_auto_bulk(monkeypatch):
    responses = []
    initial = [{
        "headings": ["col1"],
        "results": [{"col1": 1}],
        "count": 2,
        "results_id": "rid",
        "next_offset": 1
    }]
    second = [{
        "results": [{"col1": 2}]
    }]
    responses.extend([DummyResponse(initial), DummyResponse(second)])

    def fake_search_once(self, query, offset=None, results_id=None, format=None, limit=100, delete=False):
        return responses.pop(0)

    monkeypatch.setattr(Data, "_search_once", fake_search_once)

    d = Data("host", "token")
    result = d.search("query")
    assert result == [["col1"], {"col1": 1}, {"col1": 2}]
    assert responses == []


def test_search_record_limit(monkeypatch):
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

    def fake_search_once(self, query, offset=None, results_id=None, format=None, limit=100, delete=False):
        return responses.pop(0)

    monkeypatch.setattr(Data, "_search_once", fake_search_once)

    d = Data("host", "token")
    result = d.search("query", record_limit=2)
    assert result == [["col1"], {"col1": 1}, {"col1": 2}]
    assert len(responses) == 1  # record_limit stops early


def test_search_call_limit(monkeypatch):
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
    call_count = {"n": 0}

    def fake_search_once(self, query, offset=None, results_id=None, format=None, limit=100, delete=False):
        call_count["n"] += 1
        return responses.pop(0)

    monkeypatch.setattr(Data, "_search_once", fake_search_once)

    d = Data("host", "token")
    result = d.search("query", call_limit=0)
    assert result == [["col1"], {"col1": 1}, {"col1": 2}]
    assert call_count["n"] == 1
    assert len(responses) == 1
