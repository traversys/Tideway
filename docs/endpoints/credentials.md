---
sort: 3
---

# Credentials

Initiate a Credential object for the instance of Discovery you intend to query.

Syntax:

```
tideway.credentials(__target__, __token__ [, _api_version_ ] [, _ssl_verify_ ])
```

Initiation:

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> credentials = tw.credentials()
```

## get_vault_credential_type()

Get a list of all credential types and filter by group and/or category.

Syntax:

```
.get_vault_credential_type([ _group_ ] [, _category_ ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| group         | String      | No       | N/A           | N/A      |
| category      | String      | No       | N/A           | N/A      |

Example:

```python
>>> db_creds = credentials.get_vault_credential_type(category="Database")
>>> from pprint import pprint
>>> pprint(db_creds.json())
[
    {
        "categories": [
            "Database"
        ],
        "description": "Database Credentials",
        "groups": [
            "OTHER"
        ],
        "label": "JDBC Export",
        "name": "jdbcexport",
        "uri": "https://appliance-hostname/api/v1.1/vault/credential_types/jdbcexport"
    },
...
```

## get_vault_credential_types

List all credential types. See [get_vault_credential_type](#get_vault_credential_type).

## get_vault_credential_type_name()

Get the properties of a specific credential type.

Syntax:

```
.get_vault_credential_type_name(__cred_type_name__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| cred_type_name | String     | Yes      | N/A           | N/A      |

```python
>>> ora_creds.credentials.get_vault_credential_type_name("oracle").json()
>>> from pprint import pprint
>>> pprint(ora_creds.json())
{
    "categories": [
        "Database Credentials"
    ],
    "description": "Oracle Database Discovery",
    "groups": [
        "SCANNING",
        "DATASOURCE"
    ],
    "label": "Oracle",
    "name": "oracle",
    "uri": "https://appliance-hostname/api/v1.1/vault/credential_types/oracle"
}
```

## get_vault_credential()

Get a list of credentials.

Syntax:

```
.get_vault_credential([ _uuid_ ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| uuid          | String      | No       | N/A           | N/A      |

Example:

```python
>>> creds = credentials.get_vault_credential("e7f00000106c1")
>>> print(creds.json()['types'])
['ssh']
```

## get_vault_credentials

List all vault credentials. See [get_vault_credential](#get_vault_credential).

## post_vault_credential()

Create a new credential.

Syntax:

```
.post_vault_credential(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |

Example:

```python
>>> credentials.post_vault_credential({"enabled": True,"username": "discovery_service","password": "password","label": "SSH Service Account","description": "Service Account for SSH","ip_range": "0.0.0.0/0,::/0","types": ["ssh"]}).ok
True
```

## delete_vault_credential()

Delete a credential.

Syntax:
```
.delete_vault_credential([ _uuid_ ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| uuid          | String      | Yes      | N/A           | N/A      |

Example:

```python
>>> credentials.delete_vault_credential("e7f00000106c1").ok
True
```

## patch_vault_credential()

Updates partial resources of a credential. Missing properties are left unchanged.

Syntax:
```
.patch_vault_credential(__uuid__, __json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| uuid          | String      | Yes      | N/A           | N/A      |
| json          | JSON Object | Yes      | N/A           | N/A      |

Example:

```python
>>> credentials.patch_vault_credential("a1b2c3d4e5f6",{ "enabled" : False }).ok
True
```

## put_vault_credential()

Replaces a single credential.

```note
All required credential properties must be present. Optional properties that are missing will be reset to their defaults.
```

Syntax:
```
.put_vault_credential(__uuid__, __json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| uuid          | String      | Yes      | N/A           | N/A      |
| json          | JSON Object | Yes      | N/A           | N/A      |

Example:

```python
>>> credentials.put_vault_credential("a1b2c3d4e5f6",{"enabled": True,"username": "discovery_service","password": "password","label": "Limited SSH Discovery","description": "Limited SSH Service Account","ip_range": "192.168.1.0/24","types":["ssh"]}).ok
True
```

## listCredentialTypes()

[Deprecated] See [get_vault_credential_type](#get_vault_credential_type) for usage.

Syntax: `.listCredentialTypes([ _group_ ] [, _category_ ])`

## credentialType()

[Deprecated] See [get_vault_credential_type_name](#get_vault_credential_type_name) for usage.

Syntax: `.credentialType(__cred_type_name__)`

## listCredentials()

[Deprecated] See [get_vault_credential](#get_vault_credential) for usage.

Syntax: `.listCredentials([ _uuid_ ])`

## newCredential()

[Deprecated] See [post_vault_credential](#post_vault_credential) for usage.

Syntax: `.newCredential(__json__)`

## deleteCredential()

[Deprecated] See [delete_vault_credential](#delete_vault_credential) for usage.

Syntax: `.deleteCredential([ _uuid_ ])`

## updateCredential()

[Deprecated] See [patch_vault_credential](#patch_vault_credential) for usage.

Syntax: `.updateCredential(__uuid__, __json__)`

## replaceCredential()

[Deprecated] See [put_vault_credential](#put_vault_credential) for usage.

Syntax: `.replaceCredential(__uuid__, __json__)`