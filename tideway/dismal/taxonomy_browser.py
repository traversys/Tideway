# Taxonomy browser helpers for DisMAL

import json
import logging
import os
from typing import Any, Dict, Iterable, List, Optional, Tuple

import tideway
from tabulate import tabulate

from . import api as api_client, output

logger = logging.getLogger("_taxonomy_browser_")

DEFAULT_CACHE_NAME = os.path.join("taxonomy", "taxonomy_cache.json")


def ensure_taxonomy_cache(api_target, cache_path: str, refresh: bool = False) -> Optional[str]:
    """Fetch and store the nodekinds list if the cache is missing or refresh is requested."""

    if not cache_path:
        return None

    if not refresh and os.path.exists(cache_path):
        return cache_path

    taxonomy_client = _taxonomy_client(api_target)
    node_list: List[str] = []
    try:
        node_list_raw = api_client.get_json(taxonomy_client.get_taxonomy_nodekind())
        if isinstance(node_list_raw, list):
            node_list = [str(n) for n in node_list_raw]
        elif isinstance(node_list_raw, dict):
            node_list = [str(k) for k in node_list_raw.keys()]
    except Exception as exc:  # pragma: no cover - network errors
        logger.warning("Failed to fetch taxonomy nodekinds for cache: %s", exc)
        return None

    cache_data = {"nodekinds": node_list, "nodes": {}}
    try:
        cache_dir = os.path.dirname(cache_path) or "."
        os.makedirs(cache_dir, exist_ok=True)
        with open(cache_path, "w") as f:
            json.dump(cache_data, f, indent=2)
    except Exception as exc:
        logger.warning("Failed to write taxonomy cache to %s: %s", cache_path, exc)
        return None

    return cache_path


def crawl_all(api_target, cache_path: str, refresh: bool = False) -> Dict[str, int]:
    """Fetch and cache every nodekind. Returns summary counts."""

    if not cache_path:
        return {"fetched": 0, "cached": 0, "total": 0}

    cache_dir = os.path.dirname(cache_path) or "."
    os.makedirs(cache_dir, exist_ok=True)

    cache_data: Dict[str, Any] = {"nodekinds": [], "nodes": {}}
    if os.path.exists(cache_path) and not refresh:
        try:
            with open(cache_path, "r") as f:
                loaded = json.load(f)
                if isinstance(loaded, dict):
                    cache_data.update(loaded)
        except Exception:
            logger.warning("Failed to read existing taxonomy cache; rebuilding.")

    taxonomy_client = _taxonomy_client(api_target)

    node_list = cache_data.get("nodekinds") or []
    if refresh or not node_list:
        try:
            node_list_raw = api_client.get_json(taxonomy_client.get_taxonomy_nodekind())
            if isinstance(node_list_raw, list):
                node_list = [str(n) for n in node_list_raw]
            elif isinstance(node_list_raw, dict):
                node_list = [str(k) for k in node_list_raw.keys()]
            cache_data["nodekinds"] = node_list
        except Exception as exc:
            logger.error("Failed to retrieve taxonomy nodekinds list: %s", exc)
            return {"fetched": 0, "cached": len(cache_data.get("nodes", {})), "total": len(node_list)}

    nodes_cache = cache_data.get("nodes") or {}
    fetched = 0
    for kind in node_list:
        if not refresh and kind in nodes_cache and nodes_cache.get(kind):
            continue
        try:
            node_payload = api_client.get_json(
                taxonomy_client.get_taxonomy_nodekind(kind=kind)
            )
            nodes_cache[kind] = node_payload
            fetched += 1
        except Exception as exc:
            logger.warning("Failed to fetch taxonomy nodekind %s: %s", kind, exc)

    cache_data["nodes"] = nodes_cache
    try:
        with open(cache_path, "w") as f:
            json.dump(cache_data, f, indent=2)
    except Exception as exc:
        logger.warning("Failed to write taxonomy cache to %s: %s", cache_path, exc)

    return {"fetched": fetched, "cached": len(nodes_cache), "total": len(node_list)}


def _taxonomy_client(api_target):
    """Return a taxonomy client derived from the current appliance object."""

    return tideway.taxonomy(
        api_target.target,
        api_target.token,
        limit=getattr(api_target, "default_limit", 100),
        api_version=getattr(api_target, "api_version", "1.14"),
        ssl_verify=getattr(api_target, "verify", False),
    )


def _stringify(value: Any) -> str:
    if isinstance(value, (list, dict)):
        try:
            return json.dumps(value, sort_keys=True)
        except Exception:
            return str(value)
    if value is None:
        return ""
    return str(value)


def _normalize_entries(raw: Any) -> List[Dict[str, Any]]:
    """Coerce taxonomy payload chunks into a uniform list of dictionaries."""

    entries: List[Dict[str, Any]] = []
    if raw is None:
        return entries

    if isinstance(raw, dict):
        for name, detail in raw.items():
            if isinstance(detail, dict):
                entry = {"name": name}
                entry.update(detail)
                entries.append(entry)
            else:
                entries.append({"name": name, "value": detail})
    elif isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict):
                entry = dict(item)
                if "name" not in entry and "Name" in entry:
                    entry["name"] = entry.get("Name")
                entries.append(entry)
            else:
                entries.append({"name": str(item)})
    else:
        entries.append({"name": str(raw)})

    return entries


def _deduplicate(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    unique: List[Dict[str, Any]] = []
    for entry in entries:
        key = json.dumps(entry, sort_keys=True, default=str)
        if key in seen:
            continue
        seen.add(key)
        unique.append(entry)
    return unique


def _extract_chunks(payload: Any, keywords: Iterable[str]) -> List[Any]:
    """Collect all values where the key contains any of the keywords."""

    chunks: List[Any] = []
    stack = [payload]
    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            for key, value in current.items():
                if value is None:
                    continue
                if any(word in key.lower() for word in keywords):
                    chunks.append(value)
                if isinstance(value, (dict, list)):
                    stack.append(value)
        elif isinstance(current, list):
            stack.extend(current)
    return chunks


def _collect_entries(sources: List[Dict[str, Any]], keywords: Iterable[str]) -> List[Dict[str, Any]]:
    collected: List[Dict[str, Any]] = []
    for source in sources:
        for chunk in _extract_chunks(source, keywords):
            collected.extend(_normalize_entries(chunk))
    return _deduplicate(collected)


def _find_node_matches(payload: Dict[str, Any], node_name: str) -> List[Tuple[Dict[str, Any], str]]:
    """Return all dicts matching the node name along with their path."""

    matches: List[Tuple[Dict[str, Any], str]] = []
    if not payload:
        return matches

    target = node_name.lower()
    stack: List[Tuple[str, Any]] = [("root", payload)]
    while stack:
        path, current = stack.pop()
        if isinstance(current, dict):
            name_val = current.get("name") or current.get("kind")
            if isinstance(name_val, str) and name_val.lower() == target:
                matches.append((current, path))
            for key, value in current.items():
                next_path = f"{path}.{key}" if path else key
                stack.append((next_path, value))
        elif isinstance(current, list):
            for idx, item in enumerate(current):
                stack.append((f"{path}[{idx}]", item))
    return matches


def _matches(value: Any, needle: str) -> bool:
    return isinstance(value, str) and needle.lower() in value.lower()


def _filter_relationships(
    entries: List[Dict[str, Any]], related_node: Optional[str] = None, role: Optional[str] = None
) -> List[Dict[str, Any]]:
    if not related_node and not role:
        return entries

    filtered: List[Dict[str, Any]] = []
    related_lc = related_node.lower() if related_node else None
    for entry in entries:
        data = entry if isinstance(entry, dict) else {"name": str(entry)}

        if related_node:
            spec = data.get("spec")
            tail_match = False
            if isinstance(spec, str):
                tail = spec.split(":")[-1].lower()
                tail_match = tail == related_lc

            # When related_node is supplied, require the spec tail to match.
            if not tail_match:
                continue

        if role:
            role_fields = [
                data.get("role"),
                data.get("relationship"),
                data.get("name"),
                data.get("label"),
                data.get("reltype"),
                data.get("relationship_type"),
                data.get("spec"),
                data.get("relationship_name"),
            ]
            if not any(_matches(field, role) for field in role_fields):
                continue

        filtered.append(entry)

    return filtered


def _format_table(entries: List[Dict[str, Any]], preferred_keys: List[str]) -> Optional[str]:
    if not entries:
        return None

    keys: List[str] = []
    for key in preferred_keys:
        if any(isinstance(entry, dict) and key in entry for entry in entries):
            keys.append(key)

    for entry in entries:
        if isinstance(entry, dict):
            for key in entry.keys():
                if key not in keys:
                    keys.append(key)

    if not keys:
        keys = ["name"]

    rows = []
    for entry in entries:
        if not isinstance(entry, dict):
            entry = {"name": entry}
        rows.append([_stringify(entry.get(key, "")) for key in keys])

    headers = [k.replace("_", " ").title() for k in keys]
    return tabulate(rows, headers=headers, tablefmt="github")


def render_taxonomy(
    api_target,
    node_name: str,
    mode: str = "attributes",
    related_node: Optional[str] = None,
    role: Optional[str] = None,
    output_json: bool = True,
    cache_path: Optional[str] = None,
    refresh_cache: bool = False,
) -> str:
    """Return taxonomy details for the selected node (JSON by default)."""

    cache_data: Dict[str, Any] = {"nodekinds": [], "nodes": {}}
    cache_dirty = False

    if cache_path and not refresh_cache and os.path.exists(cache_path):
        try:
            with open(cache_path, "r") as f:
                loaded = json.load(f)
                if isinstance(loaded, dict):
                    cache_data.update(loaded)
        except Exception:
            logger.warning("Failed to read taxonomy cache at %s; will refresh.", cache_path)
            cache_data = {"nodekinds": [], "nodes": {}}

    taxonomy_client = _taxonomy_client(api_target)
    # Build node list for fuzzy matching
    node_list = cache_data.get("nodekinds") or []
    if refresh_cache or not node_list:
        try:
            node_list_raw = api_client.get_json(taxonomy_client.get_taxonomy_nodekind())
            if isinstance(node_list_raw, list):
                node_list = [str(n) for n in node_list_raw]
            elif isinstance(node_list_raw, dict):
                node_list = [str(k) for k in node_list_raw.keys()]
            cache_data["nodekinds"] = node_list
            cache_dirty = True
        except Exception as exc:  # pragma: no cover - network errors
            logger.error("Failed to retrieve /taxonomy/nodekinds list: %s", exc)
            node_list = cache_data.get("nodekinds") or []

    selected_kind = None
    if node_list:
        for candidate in node_list:
            if candidate.lower() == node_name.lower():
                selected_kind = candidate
                break
        if selected_kind is None:
            fuzzy = [n for n in node_list if _matches(n, node_name)]
            if len(fuzzy) == 1:
                selected_kind = fuzzy[0]
            elif len(fuzzy) > 1:
                suggestions = "\n".join(sorted(fuzzy))
                if output_json:
                    return json.dumps(
                        {
                            "message": f"No exact match for '{node_name}'.",
                            "candidates": sorted(fuzzy),
                        },
                        indent=2,
                    )
                return "\n".join(
                    [
                        f"No exact match for '{node_name}'. Found {len(fuzzy)} candidates:",
                        suggestions,
                        "Re-run with one of the above names.",
                    ]
                )
    if selected_kind is None:
        selected_kind = node_name

    node_cache = cache_data.get("nodes") or {}
    node_payload = None if refresh_cache else node_cache.get(selected_kind)

    if node_payload is None:
        try:
            node_payload = api_client.get_json(
                taxonomy_client.get_taxonomy_nodekind(kind=selected_kind)
            )
            if isinstance(node_cache, dict):
                node_cache[selected_kind] = node_payload
                cache_data["nodes"] = node_cache
                cache_dirty = True
        except Exception as exc:  # pragma: no cover - network errors
            logger.error("Failed to retrieve nodekind for %s: %s", selected_kind, exc)
            node_payload = node_cache.get(selected_kind, {})

    def _attributes(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for source_key, source_label in [
            ("attrs", "declared"),
            ("inherited_attrs", "inherited"),
            ("extension_attrs", "extension"),
        ]:
            items = payload.get(source_key) or []
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        entry = dict(item)
                        entry["source"] = source_label
                        results.append(entry)
                    else:
                        results.append({"name": str(item), "source": source_label})
            elif isinstance(items, dict):
                for name, detail in items.items():
                    entry = {"name": name, "source": source_label}
                    if isinstance(detail, dict):
                        entry.update(detail)
                    results.append(entry)
        return results

    def _expressions(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for key in ("exprs", "inherited_exprs"):
            items = payload.get(key) or []
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        results.append(dict(item))
        return results

    def _parse_spec(spec: str) -> Dict[str, Any]:
        info: Dict[str, Any] = {"spec": spec}
        if not isinstance(spec, str):
            return info
        parts = spec.split(":")
        if len(parts) >= 4:
            info["from_role"] = parts[0]
            info["relationship_name"] = parts[1]
            info["to_role"] = parts[2]
            info["target_kind"] = parts[3]
        return info

    def _relationships(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for key in ("rels", "inherited_rels", "display_rels", "inherited_display_rels"):
            items = payload.get(key) or []
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        entry = dict(item)
                        spec_info = _parse_spec(entry.get("spec"))
                        entry.update(spec_info)
                        results.append(entry)
        return results

    attributes = _attributes(node_payload)
    relationships = _filter_relationships(
        _relationships(node_payload), related_node=related_node, role=role
    )
    expressions = _expressions(node_payload)

    if related_node and (mode is None or mode.lower() == "attributes"):
        mode = "relationships"

    mode_key = (mode or "attributes").lower()
    if mode_key not in ("attributes", "relationships", "expressions"):
        mode_key = "attributes"

    if output_json:
        filters = {}
        if related_node:
            filters["related_node"] = related_node
        if role:
            filters["role"] = role
        result = {
            "selected_kind": selected_kind,
            "source": f"/taxonomy/nodekinds/{selected_kind}",
            "mode": mode_key,
            "filters": filters or None,
        }

        if mode_key == "relationships":
            result["relationships"] = relationships
            result["count"] = len(relationships)
        elif mode_key == "expressions":
            result["expressions"] = expressions
        else:
            result["attributes"] = attributes

        # Only attach the full payload when no relationship filter is in play to
        # avoid dumping the entire taxonomy when a targeted lookup was requested.
        if not related_node and not role:
            result["payload"] = node_payload or {}

        if cache_dirty and cache_path:
            try:
                cache_dir = os.path.dirname(cache_path) or "."
                os.makedirs(cache_dir, exist_ok=True)
                with open(cache_path, "w") as f:
                    json.dump(cache_data, f, indent=2)
            except Exception as exc:
                logger.warning("Failed to save taxonomy cache to %s: %s", cache_path, exc)

        return json.dumps(result, indent=2)

    # Legacy table output path
    if mode_key == "relationships":
        entries = relationships
        preferred = [
            "display_name",
            "relationship_name",
            "from_role",
            "to_role",
            "target_kind",
            "description",
            "impact_from",
            "impact_to",
            "spec",
        ]
    elif mode_key == "expressions":
        entries = expressions
        preferred = ["name", "expression", "value"]
    else:
        entries = attributes
        preferred = ["name", "type", "display_name", "description", "source"]

    table = _format_table(entries, preferred_keys=preferred)

    header = f"Taxonomy for {selected_kind} [{mode_key}]"
    filters = []
    if related_node:
        filters.append(f"related node contains '{related_node}'")
    if role:
        filters.append(f"role/relationship contains '{role}'")
    if filters:
        header += " | " + "; ".join(filters)

    lines = [header]

    if node_list and selected_kind not in node_list:
        lines.append("Selected kind was not in the retrieved nodekinds list; showing raw response.")

    if not node_payload:
        lines.append("Warning: /taxonomy/nodekinds returned no data for this node.")

    lines.append("")
    if table:
        lines.append(table)
    else:
        lines.append(f"No {mode_key} found for {node_name}.")

    return "\n".join(lines)


def run(api_target, args, reporting_dir: Optional[str]):
    """Generate a taxonomy report and honour DisMAL output options."""

    node_name = args.taxonomy
    cache_path = getattr(args, "taxonomy_cache", None) or os.path.join(
        os.getcwd(), DEFAULT_CACHE_NAME
    )

    report = render_taxonomy(
        api_target,
        node_name,
        mode=getattr(args, "taxonomy_mode", "attributes"),
        related_node=getattr(args, "taxonomy_related", None),
        role=getattr(args, "taxonomy_role", None),
        output_json=True,
        cache_path=cache_path,
        refresh_cache=getattr(args, "taxonomy_refresh", False),
    )

    safe_name = node_name.replace("/", "_")
    target_dir = reporting_dir or os.getcwd()
    filename = os.path.join(target_dir, f"taxonomy_{safe_name}.txt")
    # Default behaviour for taxonomy: show in CLI unless explicitly suppressed.
    cli_out = getattr(args, "output_cli", False)
    null_out = getattr(args, "output_null", False)
    if not cli_out and not null_out:
        print(report)
    output.define_txt(args, report, filename, None)
