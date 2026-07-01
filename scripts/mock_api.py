#!/usr/bin/env python3
"""Build and run a Prism mock for the BMC Discovery API."""

import argparse
import copy
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_TARGET = "192.168.1.164"
DEFAULT_PORT = 4010
DEFAULT_HOST = "127.0.0.1"
DEFAULT_ENV_FILE = ".env"
DEFAULT_TOKEN_KEY = "BEARER"
MOCK_DIR = Path("mock")
GENERATED_DIR = MOCK_DIR / "generated"
EXAMPLES_FILE = MOCK_DIR / "examples" / "overlay.json"
RAW_SPEC_FILE = GENERATED_DIR / "openapi.raw.json"
ABOUT_FILE = GENERATED_DIR / "about.json"
PRISM_SPEC_FILE = GENERATED_DIR / "openapi.prism.json"


def load_dotenv(path):
    values = {}
    env_path = Path(path)
    if not env_path.exists():
        return values

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export ") :]
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("'\"")
    return values


def read_token(env_file, token_key):
    return os.environ.get(token_key) or load_dotenv(env_file).get(token_key)


def version_key(version):
    return tuple(int(part) for part in str(version).split("."))


def latest_api_version(about):
    versions = about.get("api_versions") or []
    if not versions:
        raise ValueError("No api_versions found in /api/about response")
    return max(versions, key=version_key)


def get_json(url, token=None, verify=False, timeout=30):
    import requests

    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    response = requests.get(url, headers=headers, verify=verify, timeout=timeout)
    response.raise_for_status()
    return response.json()


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def fetch_command(args):
    import requests

    token = read_token(args.env_file, args.token_key)
    if not token:
        raise SystemExit(f"Missing {args.token_key} in environment or {args.env_file}")

    base_url = args.target.rstrip("/")
    if not base_url.startswith(("http://", "https://")):
        base_url = "https://" + base_url

    requests.packages.urllib3.disable_warnings()
    about = get_json(f"{base_url}/api/about", token=token, verify=args.ssl_verify)
    api_version = args.api_version or latest_api_version(about)
    spec = get_json(f"{base_url}/api/v{api_version}/openapi.json", token=token, verify=args.ssl_verify)

    write_json(args.about_file, about)
    write_json(args.raw_spec_file, spec)
    print(f"Fetched BMC Discovery {about.get('product_version', about.get('version'))} API v{api_version}")
    print(f"Wrote {args.about_file}")
    print(f"Wrote {args.raw_spec_file}")


def normalize_spec_path(path, api_version):
    if not path.startswith("/"):
        path = "/" + path
    if path.startswith("/api/"):
        return path
    return f"/api/v{api_version}{path}"


def about_operation(about):
    return {
        "get": {
            "tags": ["admin"],
            "summary": "Get API about information",
            "security": [],
            "responses": {
                "200": {
                    "description": "API about information",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "additionalProperties": True,
                                "properties": {
                                    "product": {"type": "string"},
                                    "component": {"type": "string"},
                                    "version": {"type": "string"},
                                    "api_versions": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                    "product_version": {"type": "string"},
                                },
                            },
                            "example": about,
                        }
                    },
                }
            },
        }
    }


def apply_examples(spec, overlay, api_version):
    for entry in overlay.get("examples", []):
        path = normalize_spec_path(entry["path"], api_version)
        method = entry["method"].lower()
        status = str(entry.get("status", "200"))
        content_type = entry.get("content_type", "application/json")
        example = entry["example"]

        operation = spec.setdefault("paths", {}).setdefault(path, {}).setdefault(method, {})
        responses = operation.setdefault("responses", {})
        response = responses.setdefault(status, {"description": "Example response"})
        content = response.setdefault("content", {})
        media = content.setdefault(content_type, {})
        media["example"] = example


def transform_spec(raw_spec, about, overlay, api_version):
    spec = copy.deepcopy(raw_spec)
    spec["servers"] = [{"url": "/"}]

    paths = {}
    for path, operations in spec.get("paths", {}).items():
        paths[normalize_spec_path(path, api_version)] = operations
    spec["paths"] = paths
    spec["paths"]["/api/about"] = about_operation(about)

    apply_examples(spec, overlay, api_version)
    return spec


def build_command(args):
    raw_spec = json.loads(args.raw_spec_file.read_text(encoding="utf-8"))
    about = json.loads(args.about_file.read_text(encoding="utf-8"))
    overlay = json.loads(args.examples_file.read_text(encoding="utf-8"))
    api_version = args.api_version or latest_api_version(about)

    spec = transform_spec(raw_spec, about, overlay, api_version)
    write_json(args.output_file, spec)
    print(f"Built Prism spec with {len(spec.get('paths', {}))} paths")
    print(f"Wrote {args.output_file}")


def prism_command():
    prism = shutil.which("prism")
    if prism:
        return [prism]

    npx = shutil.which("npx")
    if npx:
        return [npx, "--yes", "@stoplight/prism-cli"]

    raise SystemExit("Could not find prism or npx. Install @stoplight/prism-cli or add npx to PATH.")


def run_command(args):
    if not args.spec_file.exists():
        raise SystemExit(f"Missing {args.spec_file}; run the build command first")

    command = prism_command() + [
        "mock",
        str(args.spec_file),
        "--host",
        args.host,
        "--port",
        str(args.port),
    ]
    if args.dynamic:
        command.append("--dynamic")

    print("Running " + " ".join(command))
    subprocess.run(command, check=True)


def parser():
    root = argparse.ArgumentParser(description=__doc__)
    subcommands = root.add_subparsers(dest="command", required=True)

    fetch = subcommands.add_parser("fetch", help="Fetch /api/about and /openapi.json from an appliance")
    fetch.add_argument("--target", default=DEFAULT_TARGET, help="Appliance host or URL")
    fetch.add_argument("--api-version", help="API version to fetch; defaults to latest from /api/about")
    fetch.add_argument("--env-file", default=DEFAULT_ENV_FILE, help="Path to .env containing BEARER")
    fetch.add_argument("--token-key", default=DEFAULT_TOKEN_KEY, help="Token environment variable name")
    fetch.add_argument("--ssl-verify", action="store_true", help="Verify appliance TLS certificates")
    fetch.add_argument("--about-file", type=Path, default=ABOUT_FILE)
    fetch.add_argument("--raw-spec-file", type=Path, default=RAW_SPEC_FILE)
    fetch.set_defaults(func=fetch_command)

    build = subcommands.add_parser("build", help="Build a Prism-ready OpenAPI document")
    build.add_argument("--api-version", help="API version for path prefixing; defaults to latest from about file")
    build.add_argument("--about-file", type=Path, default=ABOUT_FILE)
    build.add_argument("--raw-spec-file", type=Path, default=RAW_SPEC_FILE)
    build.add_argument("--examples-file", type=Path, default=EXAMPLES_FILE)
    build.add_argument("--output-file", type=Path, default=PRISM_SPEC_FILE)
    build.set_defaults(func=build_command)

    run = subcommands.add_parser("run", help="Run Prism against the generated spec")
    run.add_argument("--spec-file", type=Path, default=PRISM_SPEC_FILE)
    run.add_argument("--host", default=DEFAULT_HOST)
    run.add_argument("--port", type=int, default=DEFAULT_PORT)
    run.add_argument("--dynamic", action="store_true", help="Ask Prism to generate dynamic schema examples")
    run.set_defaults(func=run_command)

    return root


def main(argv=None):
    args = parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main(sys.argv[1:])
