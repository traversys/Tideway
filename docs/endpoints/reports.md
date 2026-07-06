---
sort: 13
---

# Reports

Dismal reports are available from an appliance object through `reports()`.
Report methods use normal Tideway-style parameters.

```python
import tideway

tw = tideway.appliance("appliance.example.com", "token")

result = tw.reports().credential_success()
result.headers
result.rows
```

Reports return in-memory result objects by default and do not write files.

```python
tw.reports().devices(include_endpoints=["10.0.0.1"])
tw.reports().missing_vms(resolve_hostnames=True)
tw.reports().suggested_cred_opt()
```

To write a single report, pass `output_file`.

```python
tw.reports().credential_success(output_file="credential_success.csv")
```

To use Dismal's canonical filenames, pass `output_dir`.

```python
tw.reports().devices(output_dir="reports")
```

Run a report batch with `run()`.

```python
batch = tw.reports().run(names=["devices", "credential_success"], output_dir="reports")
```

Passing `names=None` or `names=["default"]` runs the default Dismal excavation report set.

Raw query export creates multiple files and requires `output_dir`.

```python
tw.reports().run(names=["credential_success"], queries=True, output_dir="reports")
```
