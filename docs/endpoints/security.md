---
sort: 13
---

# Security

Initiate a Security object for the instance of Discovery you intend to manage.

Syntax:

```
tideway.security(__target__, __token__ [, _api_version_ ] [, _ssl_verify_ ])
```

Initiation:

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> security = tw.security()
```

## get_security_ldap

Retrieve the current LDAP configuration.

Syntax:

```
.get_security_ldap
```

## put_security_ldap()

Replace the LDAP configuration.

Syntax:

```
.put_security_ldap(__json__)
```

| Parameters | Type | Required | Default Value | Options |
| ---------- | ---- | :------: | ------------- | ------- |
| json | JSON Object | Yes | N/A | N/A |

## patch_security_ldap()

Update the LDAP configuration.

Syntax:

```
.patch_security_ldap(__json__)
```

| Parameters | Type | Required | Default Value | Options |
| ---------- | ---- | :------: | ------------- | ------- |
| json | JSON Object | Yes | N/A | N/A |

## get_security_group()

Retrieve a list of groups or a specific group.

Syntax:

```
.get_security_group([ _group_name_ ])
```

| Parameters | Type | Required | Default Value | Options |
| ---------- | ---- | :------: | ------------- | ------- |
| group_name | String | No | N/A | N/A |

## post_security_group()

Create a security group.

Syntax:

```
.post_security_group(__json__)
```

| Parameters | Type | Required | Default Value | Options |
| ---------- | ---- | :------: | ------------- | ------- |
| json | JSON Object | Yes | N/A | N/A |

## patch_security_group()

Update an existing group.

Syntax:

```
.patch_security_group(__group_name__, __json__)
```

| Parameters | Type | Required | Default Value | Options |
| ---------- | ---- | :------: | ------------- | ------- |
| group_name | String | Yes | N/A | N/A |
| json | JSON Object | Yes | N/A | N/A |

## delete_security_group()

Delete a group.

Syntax:

```
.delete_security_group(__group_name__)
```

| Parameters | Type | Required | Default Value | Options |
| ---------- | ---- | :------: | ------------- | ------- |
| group_name | String | Yes | N/A | N/A |

## get_security_permission()

Retrieve permission definitions or a specific permission set.

Syntax:

```
.get_security_permission([ _permission_ ])
```

| Parameters | Type | Required | Default Value | Options |
| ---------- | ---- | :------: | ------------- | ------- |
| permission | String | No | N/A | N/A |

## get_security_user()

Retrieve a list of users or a specific user.

Syntax:

```
.get_security_user([ _username_ ])
```

| Parameters | Type | Required | Default Value | Options |
| ---------- | ---- | :------: | ------------- | ------- |
| username | String | No | N/A | N/A |

## post_security_user()

Create a new user.

Syntax:

```
.post_security_user(__json__)
```

| Parameters | Type | Required | Default Value | Options |
| ---------- | ---- | :------: | ------------- | ------- |
| json | JSON Object | Yes | N/A | N/A |

## patch_security_user()

Update a user.

Syntax:

```
.patch_security_user(__username__, __json__)
```

| Parameters | Type | Required | Default Value | Options |
| ---------- | ---- | :------: | ------------- | ------- |
| username | String | Yes | N/A | N/A |
| json | JSON Object | Yes | N/A | N/A |

## delete_security_user()

Delete a user.

Syntax:

```
.delete_security_user(__username__)
```

| Parameters | Type | Required | Default Value | Options |
| ---------- | ---- | :------: | ------------- | ------- |
| username | String | Yes | N/A | N/A |

## post_security_token()

Retrieve an authentication token for a user.

Syntax:

```
.post_security_token(__json__)
```

| Parameters | Type | Required | Default Value | Options |
| ---------- | ---- | :------: | ------------- | ------- |
| json | JSON Object | Yes | N/A | N/A |

