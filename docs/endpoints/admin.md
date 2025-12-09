---
sort: 1
---

# Admin

Initiate an Admin object for the instance of Discovery you intend to query.

Syntax:

```
tideway.admin(__target__, __token__ [, _api_version_ ] [, _ssl_verify_ ])
```

Initiation:

```python
>>> import tideway
>>> tw = tideway.admin('hostname','auth-token')
```

## get_admin_baseline

Get a summary of the appliance status, and details of which baseline checks have passed or failed.

Syntax:

```
.get_admin_baseline
```

Example:

```python
>>> tw.get_admin_baseline.json()['results']['FAILED'][0]
{'enabled': True, 'message': 'MAJOR: This appliance has insufficent resources', 'name': 'Appliance Specification', 'severity': 'MAJOR'}
```

## get_admin_about

Get the versions of the API supported by a BMC Discovery version.

Syntax:

```
.get_admin_about
```

Example:
```python
>>> tw.get_admin_about.json()
{'api_versions': ['1.0', '1.1', '1.2'], 'component': 'REST API', 'product': 'BMC Discovery', 'version': '12.2'}
```

## get_admin_licensing

Get the latest signed licensing report (plain text by default).

Syntax:

```
.get_admin_licensing
```

## get_admin_licensing_csv

Get the latest raw license data in CSV format as a zip file for offline analysis.

Syntax:

```
.get_admin_licensing_csv
```

## get_admin_licensing_raw

Get the latest license data as an encrypted raw license object for import to another appliance.

Syntax:

```
.get_admin_licensing_raw
```

## get_admin_instance

Get details about the appliance instance.

Syntax:

```
.get_admin_instance
```

Example:
```python
>>> tw.get_admin_instance.json()
{
    ...
}
```

## get_admin_cluster

Get cluster configuration and status.

Syntax:

```
.get_admin_cluster
```

Example:
```python
>>> tw.get_admin_cluster.json()
{
    ...
}
```

## get_admin_organizations

Get configured organizations.

Syntax:

```
.get_admin_organizations
```

Example:
```python
>>> tw.get_admin_organizations.json()
[
    ...
]
```

## get_admin_preferences

Get global appliance preferences.

Syntax:

```
.get_admin_preferences
```

Example:
```python
>>> tw.get_admin_preferences.json()
{
    ...
}
```

## get_admin_builtin_reports

Get built-in report definitions.

Syntax:

```
.get_admin_builtin_reports
```

Example:
```python
>>> tw.get_admin_builtin_reports.json()
[
    ...
]
```

## get_admin_custom_reports

Get custom report definitions.

Syntax:

```
.get_admin_custom_reports
```

Example:
```python
>>> tw.get_admin_custom_reports.json()
[
    ...
]
```

## get_admin_smtp

Get SMTP configuration.

Syntax:

```
.get_admin_smtp
```

Example:
```python
>>> tw.get_admin_smtp.json()
{
    ...
}
```
