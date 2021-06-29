---
sort: 1
---

# Appliance

Initiate an Appliance object for the instance of Discovery you intend to query.

Syntax:
> tideway.appliance(_target_, _token_ [, _api_version_ ] [, _ssl_verify_ ] [, _limit_ ] [, _offset_ ])

## about()

Get the versions of the API supported by a BMC Discovery version.

Example:
```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> tw.about().json()
{'api_versions': ['1.0', '1.1', '1.2'], 'component': 'REST API', 'product': 'BMC Discovery', 'version': '12.2'}
```

## admin()

Get information about the appliance, like its version and versions of the installed packages.

Syntax:

> .admin()

Example:
```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> details = tw.admin().text
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

## swagger()

Get JSON swagger file which contains the API schema.

Syntax:

> .swagger()

Example:
```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> swagger = tw.swagger()
>>> from pprint import pprint
>>> pprint(swagger.json()['tags'])
[{'description': 'Control scanning and view results', 'name': 'discovery'},
 {'description': 'Read and import data', 'name': 'data'},
 {'description': 'Manage the credential vault', 'name': 'vault'},
 {'description': 'Manage credentials', 'name': 'credentials'},
 {'description': 'Upload new TKUs and pattern modules', 'name': 'knowledge'},
 {'description': 'Push events', 'name': 'events'},
 {'description': 'Manage the BMC Discovery appliance', 'name': 'admin'},
 {'description': 'Retrieve topology data from the datastore',
  'name': 'topology'}]
```

## baseline()

- Get a summary of the appliance status, and details of which baseline checks have passed or failed.

Syntax:

> .baseline()

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> tw.baseline().json()['results']['FAILED'][0]
{'enabled': True, 'message': 'MAJOR: This appliance has insufficent resources', 'name': 'Appliance Specification', 'severity': 'MAJOR'}
```

## licensing()

Get the latest signed licensing report.

- CSV option returns raw license data in CSV format as a zip file for offline analysis.
- RAW option return an encrypted raw license object for import to another appliance.

Syntax:

> .licensing([ _content_type_ ])

| Parameters   | Type   | Required | Default Value | Options |
| ------------ | ------ | -------- | ------------- | ------- | 
| content_type | String | No       | "text/plain"  | <ul><li>"text/plain"</li><li>"csv"</li><li>"raw"</li></ul>

Example:
```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
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

> help([ _endpoint_ ])

| Parameters   | Type   | Required | Default Value | Options                                         |
| ------------ | ------ | -------- | ------------- | ----------------------------------------------- |
| endpoint     | String | No       | N/A           | Any API endpoint from Swagger UI specification. |

Example:

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> tw.help("/vault/credentials/{cred_id}")
Endpoint                      Function                          Description
----------------------------  --------------------------------  ---------------------------------------------------------------------------------
/vault/credentials/{cred_id}  deleteCredential(cred_id)         Delete a credential.
/vault/credentials/{cred_id}  listCredentials(cred_id)          Get the properties of a specific credential.
/vault/credentials/{cred_id}  updateCredential(cred_id, body)   Updates partial resources of a credential. Missing properties are left unchanged.
/vault/credentials/{cred_id}  replaceCredential(cred_id, body)  Replaces a single credential. All required credential properties must be present.

```
