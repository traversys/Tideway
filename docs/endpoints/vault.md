---
sort: 12
---

# Vault

Initiate a Vault object for the instance of Discovery you intend to manage.

Syntax:

```
tideway.vault(__target__, __token__ [, _api_version_ ] [, _ssl_verify_ ])
```

Initiation:

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> vault = tw.vault()
```

## get_vault

Get details of the state of the vault.

Syntax:

```
.get_vault
```

Example:

```python
>>> vault.get_vault.json()
{'open': True, 'passphrase_saved': False, 'passphrase_set': False}
```

## patch_vault()

Change the state of the vault.

Syntax:

```
.patch_vault(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |

Example:

```python
>>> vault.patch_vault({"open": True,"passphrase":"long pass phrase"}).ok
True
```

## getVault()

[Deprecated] See [get_vault](#get_vault) for usage.

Syntax: `.getVault()`

## updateVault()

[Deprecated] See [patch_vault](#patch_vault) for usage.

Syntax: `.updateVault(__json__)`