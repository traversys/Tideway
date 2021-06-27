---
sort: 4
---

# Vault

- Initiate a Vault object for the instance of Discovery you intend to manage.

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> vault = tw.vault()
```

## getVault()

- Get details of the state of the vault.

```python
>>> vault.getVault().json()
{'open': True, 'passphrase_saved': False, 'passphrase_set': False}
```

## updateVault(*json*)

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required

- Change the state of the vault.

```python
>>> vault.updateVault({"open": True,"passphrase": "pass phrase"})
```