---
sort: 9
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
>>> tw = tideway.admin('appliance-hostname','auth-token')
```

## baseline()

- Get a summary of the appliance status, and details of which baseline checks have passed or failed.

Syntax:

```
.baseline()
```

Example:

```python
>>> tw.baseline().json()['results']['FAILED'][0]
{'enabled': True, 'message': 'MAJOR: This appliance has insufficent resources', 'name': 'Appliance Specification', 'severity': 'MAJOR'}
```

## about()

Get the versions of the API supported by a BMC Discovery version.

Syntax:

```
.about()
```

Example:
```python
>>> tw.about().json()
{'api_versions': ['1.0', '1.1', '1.2'], 'component': 'REST API', 'product': 'BMC Discovery', 'version': '12.2'}
```

## licensing()

Get the latest signed licensing report.

- CSV option returns raw license data in CSV format as a zip file for offline analysis.
- RAW option return an encrypted raw license object for import to another appliance.

Syntax:

```
.licensing([ _content_type_ ])
```

| Parameters   | Type   | Required | Default Value | Options |
| ------------ | ------ | :------: | ------------- | ------- | 
| content_type | String | No       | "text/plain"  | <ul><li>"text/plain"</li><li>"csv"</li><li>"raw"</li></ul>

Example:
```python
>>> tw.licensing()
-----BEGIN LICENSE REPORT-----
License report
==============

Report start time: 2021-01-18 23:00:00.409987+00:00
Report end time  : 2021-01-21 23:00:00.410085+00:00
...
```