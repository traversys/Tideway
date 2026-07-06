from pathlib import Path
from typing import Any, Dict, Iterable, Optional

import pandas as pd
import yaml

import tideway
from .results import BatchReportResult, ReportResult, TextResult


def find_repo_root(start: Optional[Path] = None) -> Path:
    """Return the nearest parent containing config.yaml or .git."""

    current = (start or Path.cwd()).resolve()
    for candidate in [current] + list(current.parents):
        if (candidate / "config.yaml").exists() or (candidate / ".git").is_dir():
            return candidate
    return current


def load_config(path: Optional[str] = None) -> Dict[str, Any]:
    """Load a Tideway-style YAML config file."""

    config_path = Path(path).expanduser() if path else find_repo_root() / "config.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with config_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def selected_appliance_config(
    config: Dict[str, Any],
    appliance_name: Optional[str] = None,
    appliance_index: int = 0,
) -> Dict[str, Any]:
    """Return one appliance entry, falling back to top-level config values."""

    appliances = config.get("appliances") or []
    if isinstance(appliances, dict):
        appliances = [appliances]

    selected: Dict[str, Any] = {}
    if appliances:
        if appliance_name:
            selected = next(
                (
                    entry
                    for entry in appliances
                    if entry.get("name") == appliance_name or entry.get("target") == appliance_name
                ),
                None,
            )
            if selected is None:
                raise ValueError(f"No appliance named {appliance_name!r} in config.yaml")
        else:
            try:
                selected = appliances[int(appliance_index)]
            except (IndexError, TypeError, ValueError):
                selected = appliances[0]

    merged = dict(config)
    merged.update(selected or {})
    return merged


def token_from_config(config: Dict[str, Any], repo_root: Optional[Path] = None) -> str:
    """Read an API token from config or token_file."""

    token = str(config.get("token") or "").strip()
    if token:
        return token

    token_file = config.get("token_file") or config.get("f_token")
    if not token_file:
        raise ValueError("API token not found in config.yaml (token or token_file)")

    path = Path(token_file).expanduser()
    if not path.is_absolute():
        path = (repo_root or find_repo_root()) / path
    return path.read_text(encoding="utf-8").strip()


def appliance_from_config(
    config_path: Optional[str] = None,
    appliance_name: Optional[str] = None,
    appliance_index: int = 0,
):
    """Create a Tideway appliance from config.yaml."""

    repo_root = find_repo_root()
    config = load_config(config_path)
    selected = selected_appliance_config(config, appliance_name, appliance_index)
    target = str(selected.get("target") or "").strip()
    if not target:
        raise ValueError("config.yaml missing target")

    api_version = str(selected.get("api_version") or config.get("api_version") or "1.16")
    api_version = api_version.lstrip("v")
    verify_ssl = bool(selected.get("verify_ssl", selected.get("ssl_verify", config.get("verify_ssl", False))))
    token = token_from_config(selected, repo_root)
    return tideway.appliance(target, token, api_version=api_version, ssl_verify=verify_ssl)


def output_dir_for(target: str, base_dir: Optional[str] = None) -> Path:
    """Return the canonical output directory for a Discovery target."""

    sanitized = str(target).replace(".", "_").replace(":", "_").replace("/", "_")
    base = Path(base_dir).expanduser() if base_dir else find_repo_root()
    return base / f"output_{sanitized}"


def report_to_dataframe(result: Any) -> pd.DataFrame:
    """Convert Tideway report result objects to a DataFrame."""

    if isinstance(result, BatchReportResult):
        frames = [report_to_dataframe(item) for item in result.results]
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    if isinstance(result, ReportResult):
        return pd.DataFrame(result.rows, columns=result.headers)
    if isinstance(result, TextResult):
        return pd.DataFrame({"text": result.text.splitlines()})
    if isinstance(result, pd.DataFrame):
        return result
    if isinstance(result, Iterable) and not isinstance(result, (str, bytes, dict)):
        return pd.DataFrame(result)
    if isinstance(result, dict):
        return pd.DataFrame([result])
    return pd.DataFrame()
