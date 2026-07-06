---
sort: 14
---

# Appliance CLI

Dismal's appliance SSH commands are available through `tideway.appliance_cli()`.

```python
import tideway

with tideway.appliance_cli("appliance.example.com", password="secret") as cli:
    disk = cli.disk_info()
```

The default SSH username is `tideway`.

Methods return in-memory result objects unless an output path is supplied.

```python
cli = tideway.appliance_cli("appliance.example.com", password_file="tideway.pass")

cli.disk_info(output_file="disk.csv")
cli.certificates(output_file="certificates.txt")
cli.tw_config_dump(output_dir="reports")
```

Some commands need Discovery system credentials as well as the appliance SSH
password.

```python
cli = tideway.appliance_cli(
    "appliance.example.com",
    password="tideway-password",
    system_username="admin",
    system_password="admin-password",
)

cli.tw_options(output_file="tw_options.txt")
```

From an existing appliance object, use the convenience constructor.

```python
tw = tideway.appliance("appliance.example.com", "token")
cli = tw.appliance_cli(password="secret")
```

Destructive queue clearing requires explicit confirmation.

```python
cli.clear_queue(confirm=True)
```
