import json
import os
import hashlib

_CACHE_DIR = None
_ENABLED = True


def configure(cache_dir=None, enabled=True):
    """Configure the cache directory and enabled state."""
    global _CACHE_DIR, _ENABLED
    _CACHE_DIR = cache_dir
    _ENABLED = enabled


def is_enabled():
    """Return True if caching is enabled and a directory is set."""
    return _ENABLED and _CACHE_DIR is not None


def canonical_query(query):
    """Normalise query input into a consistent structure."""
    if isinstance(query, str):
        query = {"query": query}
    if isinstance(query, dict) and isinstance(query.get("query"), str):
        q = dict(query)
        q["query"] = q["query"].replace("\n", " ").replace("\r", " ")
        return q
    return query


def _key(name, query, limit):
    key_data = {"name": name, "query": query, "limit": limit}
    key_json = json.dumps(key_data, sort_keys=True, default=str)
    digest = hashlib.sha1(key_json.encode("utf-8")).hexdigest()
    if name:
        return f"{name}_{digest}.json"
    return f"{digest}.json"


def _path(name, query, limit):
    if _CACHE_DIR is None:
        return None
    filename = _key(name, query, limit)
    return os.path.join(_CACHE_DIR, filename)


def load(name, query, limit):
    """Load cached JSON for a query if available."""
    if not is_enabled():
        return None
    path = _path(name, canonical_query(query), limit)
    if not path or not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None


def save(name, query, limit, data):
    """Save JSON data for a query to the cache."""
    if not is_enabled():
        return
    path = _path(name, canonical_query(query), limit)
    if not path:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)
