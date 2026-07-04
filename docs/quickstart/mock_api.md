# Prism Mock API

Tideway can run against a local Prism mock built from a BMC Discovery appliance OpenAPI document. The mock workflow keeps fetched appliance files in `mock/generated/`, which is ignored by git.

## Requirements

- Python dependencies from this project, including `requests`.
- A `.env` file containing `BEARER=<token>`.
- Prism available as either `prism` on `PATH` or through `npx --yes @stoplight/prism-cli`.

## Build The Mock

Fetch the current schema from the sandbox appliance:

```bash
python scripts/mock_api.py fetch --target 192.168.1.164
```

Build a Prism-ready spec:

```bash
python scripts/mock_api.py build
```

Run Prism on `127.0.0.1:4010`:

```bash
python scripts/mock_api.py run --port 4010
```

The build step prefixes appliance paths with `/api/v1.14`, adds `/api/about`, normalizes `servers` to `/`, and overlays sanitized examples from `mock/examples/overlay.json`.

## Use With Tideway

Explicit URLs are respected, so a local HTTP Prism target works directly:

```python
import tideway

tw = tideway.appliance("http://127.0.0.1:4010", "mock-token", api_version="1.14")
print(tw.api_about.json())
print(tw.get("/admin/about").json())
```

Bare hostnames still default to HTTPS:

```python
tw = tideway.appliance("192.168.1.164", "real-token", api_version="1.14")
```

## Smoke Checks

```bash
curl http://127.0.0.1:4010/api/about
curl -H 'Authorization: Bearer mock-token' http://127.0.0.1:4010/api/v1.14/admin/about
curl -H 'Authorization: Bearer mock-token' http://127.0.0.1:4010/api/v1.14/discovery/runs
curl -H 'Authorization: Bearer mock-token' 'http://127.0.0.1:4010/api/v1.14/data/search?query=search+Host+show+name'
```
