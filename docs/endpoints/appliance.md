---
sort: 2
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
## help([ *"API Endpoint"* ])

- Get help on specific Discovery API endpoint and function to use. Outputs full list by default.

```python
>>> tw.help("/vault/credentials/{cred_id}")
Endpoint                      Function                          Description
----------------------------  --------------------------------  ---------------------------------------------------------------------------------
/vault/credentials/{cred_id}  deleteCredential(cred_id)         Delete a credential.
/vault/credentials/{cred_id}  listCredentials(cred_id)          Get the properties of a specific credential.
/vault/credentials/{cred_id}  updateCredential(cred_id, body)   Updates partial resources of a credential. Missing properties are left unchanged.
/vault/credentials/{cred_id}  replaceCredential(cred_id, body)  Replaces a single credential. All required credential properties must be present.

```