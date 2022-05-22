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

## listCredentialTypes()

Get a list of all credential types and filter by group and/or category.

Syntax:

```
.listCredentialTypes([ _group_ ] [, _category_ ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| group         | String      | No       | N/A           | N/A      |
| category      | String      | No       | N/A           | N/A      |

Example:

```python
>>> db_creds = credentials.listCredentialTypes(category="Database")
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

## credentialType()

Get the properties of a specific credential type.

Syntax:

```
.credentialType(__cred_type_name__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| cred_type_name | String     | Yes      | N/A           | N/A      |

```python
>>> ora_creds.credentials.credentialType("oracle").json()
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

## listCredentials()

Get a list of credentials.

Syntax:

```
.listCredentials([ _uuid_ ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| uuid          | String      | No       | N/A           | N/A      |

Example:

```python
>>> creds = credentials.listCredentials("e7f00000106c1")
>>> print(creds.json()['types'])
['ssh']
```

## newCredential()

Create a new credential.

Syntax:

```
.newCredential(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |

Example:

```python
>>> credentials.newCredential({"enabled": True,"username": "discovery_service","password": "password","label": "SSH Service Account","description": "Service Account for SSH","ip_range": "0.0.0.0/0,::/0","types": ["ssh"]}).ok
True
```

## deleteCredential()

Delete a credential.

Syntax:
```
.deleteCredential([ _uuid_ ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| uuid          | String      | Yes      | N/A           | N/A      |

Example:

```python
>>> credentials.deleteCredential("e7f00000106c1").ok
True
```

## updateCredential()

Updates partial resources of a credential. Missing properties are left unchanged.

Syntax:
```
.updateCredential(__uuid__, __json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| uuid          | String      | Yes      | N/A           | N/A      |
| json          | JSON Object | Yes      | N/A           | N/A      |

Example:

```python
>>> credentials.updateCredential("a1b2c3d4e5f6",{ "enabled" : False }).ok
True
```

## replaceCredential()

Replaces a single credential.

```note
All required credential properties must be present. Optional properties that are missing will be reset to their defaults.
```

Syntax:
```
.replaceCredential(__uuid__, __json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| uuid          | String      | Yes      | N/A           | N/A      |
| json          | JSON Object | Yes      | N/A           | N/A      |

Example:

```python
>>> tc.replaceCredential("a1b2c3d4e5f6",{"enabled": True,"username": "discovery_service","password": "password","label": "Limited SSH Discovery","description": "Limited SSH Service Account","ip_range": "192.168.1.0/24","types":["ssh"]}).ok
True
```