---
sort: 4
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

## getVault()

Get details of the state of the vault.

Syntax:

```
.getVault()
```

Example:

```python
>>> vault.getVault().json()
{'open': True, 'passphrase_saved': False, 'passphrase_set': False}
```

## updateVault()

Change the state of the vault.

Syntax:

```
.updateVault(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |

Example:

```python
>>> vault.updateVault({"open": True,"passphrase":"long pass phrase"}).ok
True
```