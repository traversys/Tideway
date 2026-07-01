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
.instance()
```

Example:
```python
>>> tw.instance().json()
{
    ...
}
```

## cluster()

Get cluster configuration and status.

Syntax:

```
.cluster()
```

Example:
```python
>>> tw.cluster().json()
{
    ...
}
```

## organizations()

Get configured organizations.

Syntax:

```
.organizations()
```

Example:
```python
>>> tw.organizations().json()
[
    ...
]
```

## preferences()

Get global appliance preferences.

Syntax:

```
.preferences()
```

Example:
```python
>>> tw.preferences().json()
{
    ...
}
```

## builtin_reports()

Get built-in report definitions.

Syntax:

```
.builtin_reports()
```

Example:
```python
>>> tw.builtin_reports().json()
[
    ...
]
```

## custom_reports()

Get custom report definitions.

Syntax:

```
.custom_reports()
```

Example:
```python
>>> tw.custom_reports().json()
[
    ...
]
```

## smtp()

Get SMTP configuration.

Syntax:

```
.smtp()
```

Example:
```python
>>> tw.smtp().json()
{
    ...
}
```
