---
sort: 1
---

# Appliance

- Initiate an Appliance object for the instance of Discovery you intend to query.

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
```

## about()

- Get the versions of the API supported by a BMC Discovery version.

```python
>>> tw.about()
```

## admin()

- Get information about the appliance, like its version and versions of the installed packages.

```python
>>> tw.admin()
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

- Get JSON swagger file which contains the API schema.

```python
>>> tw.swagger()
https://appliance-hostname/api/v1.1/swagger.json
{
    "swagger": "2.0",
    "info": {
        "version": "1.1",
        "title": "BMC Discovery API",
        "description": "The REST API for BMC Discovery"
    },
...
```

## baseline()

- Get a summary of the appliance status, and details of which baseline checks have passed or failed.

```python
>>> ta.baseline().json()
{
    "results": {
        "FAILED": [
            {
                "enabled": true,
                "message": "MAJOR: This appliance has insufficent resources",
                "name": "Appliance Specification",
                "severity": "MAJOR"
            },
            {
                "details": [
                    {
                        "messages": [
                            "2 credentials have been added",
...
```

## licensing()

- Get the latest signed licensing report.
- CSV option returns raw license data in CSV format as a zip file for offline analysis.
- RAW option return an encrypted raw license object for import to another appliance.

Syntax: `licensing([ content_type=*optional* (default="text/plain") ])`

| Parameters | Type | Use | Options
| - | - | - | -
| content_type=**string** | String | | "text/plain"<br>"csv"<br>"raw" |

```python
>>> ta.licensing()
-----BEGIN LICENSE REPORT-----
License report
==============

Report start time: 2021-01-18 23:00:00.409987+00:00
Report end time  : 2021-01-21 23:00:00.410085+00:00
...
```

## help()

- Get help on specific Discovery API endpoint and function to use. Outputs full list by default.

Syntax: `help([ *"API Endpoint"* ])`

```python
>>> tw.help("/vault/credentials/{cred_id}")
Endpoint                      Function                          Description
----------------------------  --------------------------------  ---------------------------------------------------------------------------------
/vault/credentials/{cred_id}  deleteCredential(cred_id)         Delete a credential.
/vault/credentials/{cred_id}  listCredentials(cred_id)          Get the properties of a specific credential.
/vault/credentials/{cred_id}  updateCredential(cred_id, body)   Updates partial resources of a credential. Missing properties are left unchanged.
/vault/credentials/{cred_id}  replaceCredential(cred_id, body)  Replaces a single credential. All required credential properties must be present.

```