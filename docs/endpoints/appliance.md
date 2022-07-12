---
sort: 2
---

# Appliance or Outpost

Initiate an Appliance or Outpost object for the instance of Discovery you intend to query.

Syntax:

```
tideway.appliance(__target__, __token__ [, _api_version_ ] [, _ssl_verify_ ] [, _limit_ ] [, _offset_ ])
tideway.outpost(__target__, __token__ [, _api_version_ ] [, _ssl_verify_ ] [, _limit_ ] [, _offset_ ])
```

Initiation:

```python
>>> import tideway
>>> tw = tideway.appliance('hostname','auth-token')
```

## api_about

Get the versions of the API supported by a BMC Discovery version.

Syntax:

```
.api_about
```

Example:
```python
>>> tw.api_about.json()
{'api_versions': ['1.0', '1.1', '1.2'], 'component': 'REST API', 'product': 'BMC Discovery', 'version': '12.2'}
```

## api_swagger

Get JSON swagger file which contains the API schema.

Syntax:

```
.api_swagger
```

Example:

```python
>>> swagger = tw.api_swagger
>>> from pprint import pprint
>>> pprint(api_swagger.json()['tags'])
[{'description': 'Control scanning and view results', 'name': 'discovery'},
 {'description': 'Read and import data', 'name': 'data'},
 {'description': 'Manage the credential vault', 'name': 'vault'},
 {'description': 'Manage credentials', 'name': 'credentials'},
 {'description': 'Upload new TKUs and pattern modules', 'name': 'knowledge'},
 {'description': 'Push events', 'name': 'events'},
 {'description': 'Manage the BMC Discovery appliance', 'name': 'admin'},
 {'description': 'Retrieve topology data from the datastore', 'name': 'topology'}]
```

## api_help

Outputs full list of help methods see [help()](#help).

## get_admin_baseline

- Get a summary of the appliance status, and details of which baseline checks have passed or failed.

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

Get information about the appliance, like its version and versions of the installed packages.

Syntax:

```
.get_admin_about
```

Example:
```python
>>> details = tw.get_admin_about.text
>>> print(details)
{
    "versions": {
        "devices": "5.0.2020.09.3",
        "os_updates": "7.20.08.25",
        "product": "12.1",
        "product_content": "2.0.2020.09.3"
    }
}
```

## get_admin_licensing

Get the latest signed licensing report in plain text.

Syntax:

```
.get_admin_licensing
```

Example:
```python
>>> tw.get_admin_licensing.text
-----BEGIN LICENSE REPORT-----
License report
==============

Report start time: 2021-01-18 23:00:00.409987+00:00
Report end time  : 2021-01-21 23:00:00.410085+00:00
...
```

## get_admin_licensing_csv

Get the latest raw license data in CSV format as a zip file for offline analysis.

Syntax:

```
.get_admin_licensing_csv
```

Example:
```python
>>> tw.get_admin_licensing_csv

```

## get_admin_licensing_raw

Get the latest license data as encrypted raw license object for import to another appliance.

Syntax:

```
.get_admin_licensing_raw
```

Example:
```python
>>> tw.get_admin_licensing_raw

```

## get()

Run a direct endpoint query using GET request.

Syntax:

```
.get(__endpoint__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| endpoint      | String      | Yes      | N/A           | N/A      |

Example:
```python
>>> tw.get("/vault")
{
    "open": true,
    "passphrase_saved": false,
    "passphrase_set": false
}
```

## post()

Run a direct endpoint query using POST.

Syntax:

```
.post(__endpoint__, __body__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| endpoint      | String      | Yes      | N/A           | N/A      |
| body          | JSON Object | Yes      | N/A           | N/A      |

Example:
```python
>>> tw.post("/data/search",{"query": "search Host show os_class process with unique()"})
[
	{
		'count': 3,
		'kind': 'Unique row',
		'offset': 0,
		'results': [
			{
				'os_class': 'UNIX'
			},
			{
				'os_class': 'Windows'
			},
			{
				'os_class': 'Other'
			}
		]
	}
]
```

## delete()

Run a direct endpoint query using DELETE. The endpoint is assumed to contain a specific identifier parsed as a string query.

Syntax:

```
.delete(__endpoint__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| endpoint      | String      | Yes      | N/A           | N/A      |

Example:
```python
>>> tw.delete("/discovery/runs/scheduled/{run_id}")

```

## patch()

Run a direct endpoint query using PATCH.

Syntax:

```
.patch(__endpoint__, __body__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| endpoint      | String      | Yes      | N/A           | N/A      |
| body          | JSON Object | Yes      | N/A           | N/A      |

Example:
```python
>>> tw.patch("/discovery/runs/scheduled/{run_id}",{"enabled": true})

```

## put()

Run a direct endpoint query using PUT.

Syntax:

```
.put(__endpoint__, __body__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| endpoint      | String      | Yes      | N/A           | N/A      |
| body          | JSON Object | Yes      | N/A           | N/A      |

Example:
```python
>>> tw.put("/vault/credentials/{cred_id}",{"enabled": true})

```

## about()

[Deprecated] See [api_about](#api_about) for usage.

Syntax: `.about()`

## admin()

[Deprecated] See [get_admin_about](#get_admin_about) for usage.

Syntax: `.admin()`

## swagger()

[Deprecated] See [api_swagger](#api_swagger) for usage.

Syntax: `.swagger()`

## baseline()

[Deprecated] See [get_admin_baseline](#get_admin_baseline) for usage.

Syntax: `.baseline()`

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

## help()

- Get help on specific Discovery API endpoint and function to use. Outputs full list by default.

Syntax:

```
.help([ _endpoint_ ])
```

| Parameters   | Type   | Required | Default Value | Options                                         |
| ------------ | ------ | :------: | ------------- | ----------------------------------------------- |
| endpoint     | String | No       | N/A           | Any API endpoint from Swagger UI specification. |

Example:

```python
>>> tw.help("/vault/credentials/{cred_id}")
Endpoint                      Function                          Description
----------------------------  --------------------------------  ---------------------------------------------------------------------------------
/vault/credentials/{cred_id}  deleteCredential(cred_id)         Delete a credential.
/vault/credentials/{cred_id}  listCredentials(cred_id)          Get the properties of a specific credential.
/vault/credentials/{cred_id}  updateCredential(cred_id, body)   Updates partial resources of a credential. Missing properties are left unchanged.
/vault/credentials/{cred_id}  replaceCredential(cred_id, body)  Replaces a single credential. All required credential properties must be present.

```