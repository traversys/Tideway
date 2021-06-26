---
sort: 1
---
# Tideway

Simplified Python library for BMC Discovery API Interface that makes use of the Python Requests module (https://github.com/psf/requests) and uses the same response handler.

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> tw.about().url
'https://appliance-hostname/api/about'
>>> tw.about().status_code
200
>>> tw.about().text
{
    "api_versions": [
        "1.0",
        "1.1",
        "1.2"
    ],
    "component": "REST API",
    "product": "BMC Discovery",
    "version": "12.2"
}
```

Tideway follows BMC Discovery's well-structured and documented REST API which can be viewed from `https://<appliance>/swagger-ui/`.

Tideway removes the extra layer of manually constructing a URL and parameters for python requests allowing you to query API supported features of Discovery seamlessly and faster than if you were to navigate via the GUI.

## Table of Contents

- [Installation](#installation)
- [Quickstart Guide](#quickstart-guide)
- [Appliance](#appliance)
- [Discovery](#discovery)
- [Data](#data)
- [Vault](#vault)
- [Credentials](#credentials)
- [Knowledge](#knowledge)
- [Events](#events)
- [Topology](#topology)

## Installation

- Tideway can be installed via PyPI:

```console
$ python -m pip install tideway
```

- Tideway supports BMC Discovery 11.3+, API v1.2 using Python 3.

## Quickstart Guide

### Object Initiation

In order to make use of an API endpoint, you will need to initiate an object representing an instance of Discovery using an authentication token (generated in the GUI) and a hostname, fqdn or ip address.

Initiating an instance is done by creating an 'appliance' object:

`tideway.appliance(<appliance>,<api_token>)`

 Or you can specify one of the following top-level endpoints:

```
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
| api_version | | String | "1.2" | This should be the supported version of the API. Discovery 12.2 supports 1.0, 1.1 and 1.2.
| ssl_verify | | Boolean | False | Choose whether to query the API using a valid SSL certificate. If you are using self-signed HTTPS then you should leave this with the default value.

### Responses

#### Input

```python
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> response = tw.about()
```

#### .headers
```
{'Date': 'Sun, 06 Jun 2021 18:43:31 GMT', 'Server': 'waitress', 'X-Content-Type-Options': 'nosniff', 'Content-Length': '160', 'Content-Type': 'application/json', 'Content-security-policy': "default-src https: 'self'; style-src https: 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline' 'unsafe-eval' blob:; img-src 'self' data:; base-uri 'none'; object-src 'none'; connect-src https: 'self'; frame-ancestors 'self';", 'Keep-Alive': 'timeout=15, max=100', 'Connection': 'Keep-Alive'}
```
#### .encoding
```
None
```
#### .elapsed
```
0:00:00.028861
```
#### .content
```
b'{\n    "api_versions": [\n        "1.0",\n        "1.1",\n        "1.2"\n    ],\n    "component": "REST API",\n    "product": "BMC Discovery",\n    "version": "12.2"\n}\n'
```
#### .cookies
```
<RequestsCookieJar[]>
```
#### .history
```
[]
```
#### .is_permanent_redirect
```
False
```
#### .is_redirect
```
False
```
#### .iter_content()
```
<generator object iter_slices at 0x7fc1252a8820>
```
#### .json()
```
{'api_versions': ['1.0', '1.1', '1.2'], 'component': 'REST API', 'product': 'BMC Discovery', 'version': '12.2'}
```
#### .url
```
https://appliance-hostname/api/about
```
#### .text
```
{
    "api_versions": [
        "1.0",
        "1.1",
        "1.2"
    ],
    "component": "REST API",
    "product": "BMC Discovery",
    "version": "12.2"
}
```
#### .status_code
```
200
```
#### .request
```
<PreparedRequest [GET]>
```
#### .reason
```
OK
```
#### .raise_for_status()
```
None
```
#### .ok
```
True
```
#### links
```
{}
```

## Appliance

- Initiate an Appliance object for the instance of Discovery you intend to query.

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
```

#### about()

- Get the versions of the API supported by a BMC Discovery version.

```python
>>> tw.about()
```

#### swagger()

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
#### help([ *"API Endpoint"* ])

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
## Discovery

- Initiate a Discovery object for the instance of Discovery you intend to query.

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> discovery = tw.discovery()
```

#### getDiscoveryStatus()

- Get the current status of the discovery process.

```python
>>> status = discovery.getDiscoveryStatus()
>>> status.json()
{
	'running': False,
	'status': 'running'
}
```

#### setDiscoveryStatus(*json*)

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required

- Start or stop the discovery process.

```python
>>> discovery.setDiscoveryStatus({"status": "running"}).ok
True
```

#### getApiProviderMetadata()

- Get metadata for the API providers currently supported by BMC Discovery.

```python
>>> discovery.getApiProviderMetadata()
```

#### getDiscoveryCloudMetaData()

- Get metadata for the cloud providers currently supported by BMC Discovery.

```python
>>> discovery.getDiscoveryCloudMetaData()
```

#### discoveryRun(*json*)

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required

- Create a new snapshot discovery run.

```python
>>> discovery.discoveryRun({
  "ranges": [ "192.168.1.0/24" ],
  "label": "Network Snapshot",
  "scan_level": "Full Discovery"
}).ok
True
```
#### getDiscoveryRuns()

- Get details of all currently processing discovery runs.

```python
>>> discovery.getDiscoveryRuns()
```
#### getDiscoveryRun(*run_id*)

| Parameters | Type | Use
| - | - | -
| **run_id** | String | Required

- Get details of specific currently processing discovery run.

```python
>>> discovery.getDiscoveryRun("1234567890").json()
[
	{
		'label': 'Network Snapshot',
		'scan_kind': 'IP',
		'scan_level': 'Full Discovery',
		'scan_type': 'Snapshot',
		'total': 254,
		'valid_ranges': '192.168.1.0/24',
		uuid:'1234567890'
	}
]
```
#### updateDiscoveryRun(*run_id*, *json*)

| Parameters | Type | Use
| - | - | -
| **run_id** | String | Required
| **json** | JSON | Required

- Update the state of a specific discovery run.

```python
>>> discovery.updateDiscoveryRun("1234567890", {"cancelled": True}).ok
True
```
#### getDiscoveryRunResults(*run_id*)

| Parameters | Type | Use
| - | - | -
| **run_id** | String | Required

- Get a summary of the results from scanning all endpoints in the run, partitioned by result type.

```python
>>> discovery.getDiscoveryRunResults("1234567890")
```
#### getDiscoveryRunResult(*run_id* [, result=*optional* (default=*"Success"*) ] [, offset=*optional* ] [, results_id=*optional* ] [, format=*optional* ] [, limit=*optional*] [, delete=*optional*])

| Parameters | Type | Use | Options | Default
| - | - | - | - | -
| **run_id** | String | Required | |
| result=**string** | String | | "Success"<br>"Skipped"<br>"NoAccess"<br>"NoResponse"<br>"Error"<br>"Dropped"
| offset=**intger** | Integer | | |
| results_id=**string** | String | | |
| format=**string** | String | | "object"
| limit=**integer** | Integer | | | 100 |
| delete=**boolean** | Boolean | | | False |

- Get a summary of the results from scanning all endpoints in the run that had a specific type of result.
- Example: Retrieve DiscoveryRuns which ended with an Error, and retrieve result rows 51-100.

```python
>>> discovery.getDiscoveryRunResult("1234567890", result="Error", offset=50, results_id="a12b3cd4e5f6", limit=50)
```
#### getDiscoveryRunInferred(*run_id*)

| Parameters | Type | Use
| - | - | -
| **run_id** | String | Required

- Get a summary of all inferred devices from a discovery run, partitioned by device type.

```python
>>> discovery.getDiscoveryRunInferred("1234567890")
```
#### getDiscoveryRunInferredKind(*run_id*, *inferred_kind* [, offset=*optional* ] [, results_id=*optional* ] [, format=*optional* ] [, limit=*optional*] [, delete=*optional*])

| Parameters | Type | Use | Options | Default
| - | - | - | - | - 
| **run_id** | String | Required | |
| **inferred_kind** | String | Required | |
| offset=**intger** | Integer | | |
| results_id=**string** | String | | |
| format=**string** | String | | "object"
| limit=**integer** | Integer | | | 100 |
| delete=**boolean** | Boolean | | | False |

- Get a summary of the devices inferred by a discovery run which have a specific inferred kind.

```python
>>> discovery.getDiscoveryRunResult("1234567890", "Host", format="object").json()
[
	{
		'count': 4,
		'kind': 'Host',
		'offset': 0,
		'results': [
			{
				'#InferredElement:Inference:Associate:DiscoveryAccess.endpoint': [
					'192.168.1.1',
					'192.168.1.2',
					'192.168.1.3',
					'192.168.1.10'
				],
				'#id': 'A1B2C3D4E5F6'
...
```
## Data

- Initiate a Data object for the instance of Discovery you intend to query.

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> data = tw.data()
```

#### search(*query* [, offset=*optional* ] [, results_id=*optional* ] [, format=*optional* ] [, limit=*optional*] [, delete=*optional*])

| Parameters | Type | Use | Options | Default
| - | - | - | - | -
| **query** | String or JSON | Required | "search string"<br>{"query":"search string"} | |
| offset=**integer** | Integer | | | |
| results_id=**string** | String | | | |
| format=**string** | String | | "object" |
| limit=**integer** | Integer | | | 100 |
| delete=**boolean** | Boolean | | | False |

- Run a search query, receiving paginated results.

```python
>>> data.search("search Host show os_type process with unique()").json()
[
	{
		'count': 12,
		'headings': [
			'os_type'
		],
		'kind': 'Unique row',
		'offset': 0,
		'results': [
			[
				'Ubuntu Linux'
			],
			[
				'Windows'
			],
			[
				'CentOS Linux'
			],
			[
				'GNU/Linux'
			],
...
```
#### search_bulk(*query* [, format=*optional* ] [, limit=*optional*] [, delete=*optional*])

| Parameters | Type | Use | Options | Default
| - | - | - | - | -
| **query** | String or JSON | Required | "search string"<br>{"query":"search string"} | |
| format=**string** | String | | "object" |
| limit=**integer** | Integer | | | 100 |
| delete=**boolean** | Boolean | | | False |

- Run a search bulk search query, will loop paginated results and return all results as a JSON list object. The function makes use of results_id and offset automatically so these are not required as arguments. May take a long time to run.

```python
>>> data.search_bulk("search Host show name", limit=500)
```
#### searchQuery(*json* [, offset=*optional* ] [, results_id=*optional* ] [, format=*optional* ] [, limit=*optional*] [, delete=*optional*])

**NOTE: This method is deprecated. You can use search() for both JSON arguments and search strings.**

| Parameters | Type | Use | Options | Default
| - | - | - | - | -
| **json** | JSON | Required | {"query":"search string"}
| offset=**intger** | Integer | | |
| results_id=**string** | String | | |
| format=**string** | String | | "object"
| limit=**integer** | Integer | | | 100 |
| delete=**boolean** | Boolean | | | False |

- An alternative to GET /data/search, for search queries which are too long for urls.

```python
>>> data.searchQuery({"query": "search Host show os_class process with unique()"}, format="object").json()
[
	{
		'count': 3,
		'kind': 'Unique row',
		'offset': 0,
		'results': [
			{
				'os_class': 'UNIX'
			},
			{
				'os_class': 'Windows'
			},
			{
				'os_class': 'Other'
			}
		]
	}
]
```
#### nodeLookup(*node_id* [, relationships=*optional* (default=*False*) ] [, traverse=*optional* ] [, flags=*optional* ])

| Parameters | Type | Use | Options
| - | - | - | -
| **node_id** | JSON | Required | |
| relationships=**boolean** | String | | True<br>False
| traverse=**string** | String | | "NodeKind:Relationship:NodeKind:Node"
| flags=**string** | String | | "include_destroyed"<br>"exclude_current" |

- Get the state of a node with specified id.

```python
>>> data.nodeLookup("a1b2c3d4e5f6")
```
#### lookupNodeKind(*kind* [, offset=*optional* ] [, results_id=*optional* ] [, format=*optional* ] [, limit=*optional*] [, delete=*optional*])

| Parameters | Type | Use | Options | Default
| - | - | - | - | -
| **kind** | String | Required | |
| offset=**intger** | Integer | | |
| results_id=**string** | String | | |
| format=**string** | String | | "object"
| limit=**integer** | Integer | | | 100 |
| delete=**boolean** | Boolean | | | False |

- Finds all nodes of a specified node kind.

```python
>>> data.lookupNodeKind("Host")
```
#### graphNode(*node_id* [, focus=*optional* (default=*"sofware-connected"*)] [, apply_rules=*optional* (default=*True*) ])

| Parameters | Type | Use | Options
| - | - | - | -
| **node_id** | JSON | Required | |
| focus=**string** | String | | "software-connected"<br>"software"<br>"infrastructure"
| apply_rules=**boolean** | Boolean | | True<br>False

- Graph data represents a set of nodes and relationships that are associated to the given node.

```python
>>> data.graphNode("a1b2c3d4e5f6")
```
#### partitions()

- Graph data represents a set of nodes and relationships that are associated to the given node.

```python
>>> td.partions()
{
  "Audit": "fb30ac60bb23b90471917ae7",
  "Conjecture": "fb30ac60bb23b9047191a1f9",
  "DDD": "fb30ac60bb23b9047191a1fa",
  "Default": "fb30ac60bb23b90471917ae5",
  "Logs": "fb30ac60bb23b9047191a1fc",
  "Taxonomy": "fb30ac60bb23b90471917ae6",
  "_System": "fb30ac60bb23b9047191a1fb"
}
```
#### candidate(*json*)

- The node object of the best candidate based on the provided parameters.

```python
>>> data.candidate({})
```
#### candidates(*json*)

- Enter parameters to identify a device, the response is a list of candidate nodes ordered by descending score.

```python
>>> data.candidates({})
```
#### twImport(*json*)

- Imports data. Returns the import UUID.
#### twWrite(*json*)

- Perform arbitrary write operations.
## Vault

- Initiate a Vault object for the instance of Discovery you intend to manage.

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> vault = tw.vault()
```
#### getVault()

- Get details of the state of the vault.

```python
>>> vault.getVault().json()
{'open': True, 'passphrase_saved': False, 'passphrase_set': False}
```
#### updateVault(*json*)

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required

- Change the state of the vault.

```python
>>> vault.updateVault({"open": True,"passphrase": "pass phrase"})
```
## Credentials

- Initiate a Credential object for the instance of Discovery you intend to query.

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> credentials = tw.credentials()
```
#### listCredentialTypes([ group=*optional* ] [, category=*optional* ])

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
#### credentialType(*cred_type_name*)

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
#### listCredentials([cred_id=*optional*])

| Parameters | Type
| - | -
| cred_id=**string** | String

- Get a list of credentials.

```python
>>> credentials.listCredentials()
```
#### newCredential(*json*)

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
#### deleteCredential(*cred_id*)

| Parameters | Type | Use
| - | - | -
| cred_id=**string** | String | Required

- Delete a credential.

```python
>>> credentials.deleteCredential("a1b2c3d4e5f6").ok
True
```
#### updateCredential(*cred_id*, *json*)

| Parameters | Type | Use
| - | - | -
| cred_id=**string** | String | Required
| **json** | String | Required

- Updates partial resources of a credential. Missing properties are left unchanged.

```python
>>> credentials.updateCredential("a1b2c3d4e5f6",{ "enabled" : False }).ok
True
```
#### replaceCredential(*cred_id*, *json*)

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
## Knowledge

- Initiate a Knowledge object for the instance of Discovery you intend to query.

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> knowledge = tw.knowledge()
```
#### getKnowledgeManagement()

- Get the current state of the appliance's knowledge, including TKU versions.

```python
>>> knowledge.getKnowledgeManagement().json()
{
    "devices": "5.0.2020.09.3",
    "latest_edp": {
        "active_count": 12,
        "inactive_count": 0,
        "modified": false,
        "name": "EDP-2020-09-3-ADDM-12.1+",
        "origin": "TKU",
        "package": "Extended Data Pack",
        "submission_date": "2020-09-11T19:52:15.165794+00:00",
        "superseded_count": 0,
        "upload_id": "fb528ec3f5afe096e4b6e6f776c6564"
    },
...
```
#### getUploadStatus()

- Get the current state of a knowledge upload.

```python
>>> knowledge.getUploadStatus().json()
{
    "error": "",
    "last_result": "success",
    "messages": [
        "Validate upload: Completed OK",
        "Load TestPattern: Uploaded TestPattern.tpl as \"TestPattern\"",
        "Load TestPattern: Completed OK",
        "Activate Pattern Modules: 1 knowledge upload activated",
        "Activate Pattern Modules: Completed OK"
    ],
    "processing": false,
    "uploading": false
}
```
#### uploadKnowledge(*filename*, *file* [, activate=*optional* (default=*True*) ] [, allow_restart=*optional* (default=*False*)])

| Parameters | Type | Use | Options
| - | - | - | -
| **filename** | String | Required | |
| **file** | String | Required | |
| activate=**boolean** | Boolean | | True<br>False |
| allow_restart=**boolean** | Boolean | | True<br>False |

- Upload a TKU or pattern module to the appliance.

```python
>>> knowledge.uploadKnowledge("TestPattern.tpl","C:/Users/User001/Documents/TestPattern.tpl")
```
## Events

- Initiate an Event object for the instance of Discovery you intend to query.

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> events = tw.events()
```
#### status(*json*)

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required |

- Returns a unique ID if the event has been recorded, otherwise an empty string is returned e.g. if the event source has been disabled.

```python
>>> events.status({"source":"Event1","type":"EventType1"}
})
```
## Topology

- Initiate a Topology object for the instance of Discovery you intend to query.

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> topo = tw.topology()
```
#### graphNode(*node_id* [, focus=*optional* (default=*"sofware-connected"*)] [, apply_rules=*optional* (default=*True*) ])

| Parameters | Type | Use | Options
| - | - | - | -
| **node_id** | JSON | Required | |
| focus=**string** | String | | "software-connected"<br>"software"<br>"infrastructure"
| apply_rules=**boolean** | Boolean | | True<br>False

- Graph data represents a set of nodes and relationships that are associated to the given node.

```python
>>> topo.graphNode("a1b2c3d4e5f6")
```
#### getNodes(*json*)

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required |

- Get topology data from one or more starting nodes.
#### getNodeKinds(*json*)

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required |

- Get nodes of the specified kinds which are related to a given set of nodes.
#### visualizationState()

- Get the current state of the visualization for the authenticated user.
#### updateVizState(*json*)

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required |

- Update one or more attributes of the current state of the visualization for the authenticated user.
#### replaceVizState(*json*)

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required |

- Update any or all of the attributes of the current state of the visualization for the authenticated user.
