---
sort: 1
---

# Object Initiation

In order to make use of an API endpoint, you will need to initiate an object representing an instance of Discovery using an authentication token (generated in the GUI) and a hostname, fqdn or ip address.

Initiating an instance is done by creating an 'appliance' object:

`tideway.appliance(<appliance>,<api_token>)`

 Or you can specify one of the following top-level endpoints:

```python
tideway.discovery()
tideway.data()
tideway.vault()
tideway.credential()
tideway.knowledge()
tideway.events()
tideway.admin()
tideway.topology()
```
Upon initiation the following parameters can be used:

| Parameter | Use | Type | Default Value | Description
| - | - | - | - | -
| target | Required | String | | The Hostname, FQDN or IP Address of the Discovery instance.
| token | Required | String | | The authentication token of the API user. It is not necessary to include the "bearer" pre-text.
| api_version | | String | "1.3" | This should be the supported version of the API. Discovery 12.3 supports API versions up to 1.3.
| ssl_verify | | Boolean | False | Choose whether to query the API using a valid SSL certificate. If you are using self-signed HTTPS then you should leave this with the default value.