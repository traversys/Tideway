---
sort: 5
---

# Credentials

- Initiate a Credential object for the instance of Discovery you intend to query.

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> credentials = tw.credentials()
```

## listCredentialTypes([ group=*optional* ] [, category=*optional* ])

| Parameters | Type
| - | -
| group=**string** | String
| category=**string** | String

- Get a list of all credential types and filter by group and/or category.

```python
>>> credentials.listCredentialTypes(category="Database").json()
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

## credentialType(*cred_type_name*)

| Parameters | Type | Use
| - | - | -
| **cred_type_name** | String | Required

- Get the properties of a specific credential type.

```python
>>> credentials.credentialType("oracle").json()
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

## listCredentials([cred_id=*optional*])

| Parameters | Type
| - | -
| cred_id=**string** | String

- Get a list of credentials.

```python
>>> credentials.listCredentials()
```

## newCredential(*json*)

| Parameters | Type | Use
| - | - | -
| **json** | String | Required

- Create a new credential.

```python
>>> credentials.newCredential({
  "enabled": True,
  "username": "discovery_service",
  "password": "password",
  "label": "SSH Service Account",
  "description": "Service Account for SSH",
  "ip_range": "0.0.0.0/0,::/0",
  "types": [
    "ssh"
  ]
}).json()
{
    "uri": "https://appliance-hostname/api/v1.1/vault/credentials/a1b2c3d4e5f6",
    "uuid": "a1b2c3d4e5f6"
}
```

## deleteCredential(*cred_id*)

| Parameters | Type | Use
| - | - | -
| cred_id=**string** | String | Required

- Delete a credential.

```python
>>> credentials.deleteCredential("a1b2c3d4e5f6").ok
True
```

## updateCredential(*cred_id*, *json*)

| Parameters | Type | Use
| - | - | -
| cred_id=**string** | String | Required
| **json** | String | Required

- Updates partial resources of a credential. Missing properties are left unchanged.

```python
>>> credentials.updateCredential("a1b2c3d4e5f6",{ "enabled" : False }).ok
True
```

## replaceCredential(*cred_id*, *json*)

| Parameters | Type | Use
| - | - | -
| cred_id=**string** | String | Required
| **json** | String | Required

- Replaces a single credential. All required credential properties must be present. Optional properties that are missing will be reset to their defaults.

```python
>>> tc.replaceCredential("a1b2c3d4e5f6",{
  "enabled": True,
  "username": "discovery_service",
  "password": "password",
  "label": "Limited SSH Discovery",
  "description": "Limited SSH Service Account",
  "ip_range": "192.168.1.0/24",
  "types": [
    "ssh"
  ]
}).ok
True
```