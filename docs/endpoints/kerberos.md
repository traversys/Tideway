---
sort: 7
---

# Kerberos

Initiate a kerberos object for the instance of Discovery you intend to query.

Syntax:

```
tideway.kerberos(__target__, __token__ [, _api_version_ ] [, _ssl_verify_ ])
```

Initiation:

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> kerberos = tw.kerberos()
```

## get_vault_kerberos_realm()

Retrieve all or specific realm.

Syntax:

```
.get_vault_kerberos_realm([ _realm_name_ ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| realm_name    | String      | No       | N/A           | N/A      |

## get_vault_kerberos_realms

Retrieve all realms. See [get_vault_kerberos_realm](#get_vault_kerberos_realm).

Syntax: `.get_vault_kerberos_realms`

## post_vault_kerberos_realm()

Create a realm and Test user credentials by attempting to acquire a new Kerberos Ticket Granting Ticket (TGT)

Syntax:

```
.post_vault_kerberos_realm(__realm_name__, __json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| realm_name    | String      | Yes      | N/A           | N/A      |
| json          | JSON Object | Yes      | N/A           | N/A      |

## delete_vault_kerberos_realm()

Delete a realm.

Syntax:
```
.delete_vault_kerberos_realm(__realm_name__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| realm_name    | String      | Yes      | N/A           | N/A      |

## patch_vault_kerberos_realm()

Update a Kerberos realm.

Syntax:
```
.patch_vault_kerberos_realm(__realm_name__, __json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| realm_name    | String      | Yes      | N/A           | N/A      |
| json          | JSON Object | Yes      | N/A           | N/A      |

## get_vault_kerberos_keytabs()

List users with a Kerberos keytab file.

Syntax:

```
.get_vault_kerberos_keytabs(__realm_name__, __username__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| realm_name    | String      | Yes      | N/A           | N/A      |
| username      | String      | Yes      | N/A           | N/A      |

## post_vault_kerberos_keytab()

Upload a Kerberos keytab file.

Syntax:

```
.post_vault_kerberos_keytab(__realm_name__, __username__, __keytab_file__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| realm_name    | String      | Yes      | N/A           | N/A      |
| username      | String      | Yes      | N/A           | N/A      |
| keytab_file   | File Object | Yes      | N/A           | N/A      |

## delete_vault_kerberos_keytab()

Delete a keytab file.

Syntax:
```
.delete_vault_kerberos_keytab(__realm_name__, __username__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| realm_name    | String      | Yes      | N/A           | N/A      |
| username      | String      | Yes      | N/A           | N/A      |

## get_vault_kerberos_ccaches()

List users with a Kerberos credential cache file.

Syntax:

```
.get_vault_kerberos_ccaches(__realm_name__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| realm_name    | String      | Yes      | N/A           | N/A      |

## post_vault_kerberos_ccache()

Upload a Kerberos credential cache file.

Syntax:

```
.post_vault_kerberos_ccache(__realm_name__, __username__, __cache_file__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| realm_name    | String      | Yes      | N/A           | N/A      |
| username      | String      | Yes      | N/A           | N/A      |
| cache_file    | File Object | Yes      | N/A           | N/A      |

## delete_vault_kerberos_ccache()

Delete a cedential cache file.

Syntax:
```
.delete_vault_kerberos_ccache(__realm_name__, __username__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| realm_name    | String      | Yes      | N/A           | N/A      |
| username      | String      | Yes      | N/A           | N/A      |