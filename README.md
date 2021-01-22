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
        "1.1"
    ],
    "component": "REST API",
    "product": "BMC Discovery",
    "version": "12.1"
}
```

Tideway follows BMC Discovery's well-structured and documented REST API which can be viewed from `https://<appliance>/swagger-ui/`.

Tideway removes the extra layer of manually constructing a URL and parameters for python requests allowing you to query API supported features of Discovery seamlessly and faster than if you were to navigate via the GUI.

## Installation

- Tideway can be installed via PyPI:

```console
$ python -m pip install tideway
```

- Tideway supports BMC Discovery 11.3+, API v1.1 using Python 3.

# Quickstart Guide

## Object Initiation

In order to make use of an API endpoint, you will need to initiate an object representing an instance of Discovery using an authentication token (generated in the GUI) and a hostname, fqdn or ip address.

Initiating an instance is done by calling one of the following top-level endpoints:

- appliance
- discovery
- data
- vault
- credential
- knowledge
- events
- admin

Upon initiation the following parameters can be used:

| Endpoints | Parameter | Use | Type | Default Value | Description
| - | - | - | - | - | -
| All | target | Required | String | | The Hostname, FQDN or IP Address of the Discovery instance.
| All | token | Required | String | | The authentication token of the API user. It is not necessary to include the "bearer" pre-text.
| /Discovery<br>/Data | limit | | Integer | 100 | This limits the amount of results returned by the API. You can use optional offset parameters on some queries in order to retrieve results in batches.
| /Discovery<br>/Data | delete | | Boolean | False | If supported, you can specify to delete the results of a function call.
| All | api_version | | String | "1.1" | This should be the supported version of the API. Discovery 12.1 supports 1.0 and 1.1.
| All | ssl_verify | | Boolean | False | Choose whether to query the API using a valid SSL certificate. If you are using self-signed HTTPS then you should leave this with the default value.


## Appliance

- Initiate an Appliance object for the instance of Discovery you intend to query.

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
```

### about()

- Get the versions of the API supported by a BMC Discovery version.

```python
>>> tw.about()
```

### swagger()

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

## Discovery

- Initiate a Discovery object for the instance of Discovery you intend to query.

```python
>>> import tideway
>>> tw = tideway.discovery('appliance-hostname','auth-token')
```

### getDiscoveryStatus()

- Get the current status of the discovery process.

```python
>>> status = tw.getDiscoveryStatus()
>>> status.json()
{
	'running': False,
	'status': 'running'
}
```

### setDiscoveryStatus(*json*)

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required

- Start or stop the discovery process.

```python
>>> tw.setDiscoveryStatus({"status": "running"}).ok
True
```

### getDiscoveryCloudMetaData()

- Get metadata for the cloud providers currently supported by BMC Discovery.

```python
>>> tw.getDiscoveryCloudMetaData()
```

### discoveryRun(*json*)

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required

- Create a new snapshot discovery run.

```python
>>> tw.discoveryRun({
  "ranges": [ "192.168.1.0/24" ],
  "label": "Network Snapshot",
  "scan_level": "Full Discovery"
}).ok
True
```

### getDiscoveryRuns()

- Get details of all currently processing discovery runs.

```python
>>> tw.getDiscoveryRuns()
```

### getDiscoveryRun(*run_id*)

| Parameters | Type | Use
| - | - | -
| **run_id** | String | Required

- Get details of specific currently processing discovery run.

```python
>>> tw.getDiscoveryRun("1234567890").json()
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

### updateDiscoveryRun(*run_id*, *json*)

| Parameters | Type | Use
| - | - | -
| **run_id** | String | Required
| **json** | JSON | Required

- Update the state of a specific discovery run.

```python
>>> tw.updateDiscoveryRun("1234567890", {"cancelled": True}).ok
True
```

### getDiscoveryRunResults(*run_id*)

| Parameters | Type | Use
| - | - | -
| **run_id** | String | Required

- Get a summary of the results from scanning all endpoints in the run, partitioned by result type.

```python
>>> tw.getDiscoveryRunResults("1234567890")
```

### getDiscoveryRunResult(*run_id* [, result=*optional* (default=*"Success"*) ] [, offset=*optional* ] [, results_id=*optional* ] [, format=*optional* ])

| Parameters | Type | Use | Options
| - | - | - | -
| **run_id** | String | Required | |
| result=**string** | String | | "Success"<br>"Skipped"<br>"NoAccess"<br>"NoResponse"<br>"Error"<br>"Dropped"
| offset=**intger** | Integer | | |
| results_id=**string** | String | | |
| format=**string** | String | | "object"

- Get a summary of the results from scanning all endpoints in the run that had a specific type of result.
- Example: Retrieve DiscoveryRuns which ended with an Error, and retrieve result rows 51-100.

```python
>>> tw = tideway.discovery('appliance-hostname','auth-token',limit=50)
>>> tw.getDiscoveryRunResult("1234567890", result="Error", offset=50, results_id="a12b3cd4e5f6")
```

### getDiscoveryRunInferred(*run_id*)

| Parameters | Type | Use
| - | - | -
| **run_id** | String | Required

- Get a summary of all inferred devices from a discovery run, partitioned by device type.

```python
>>> tw.getDiscoveryRunInferred("1234567890")
```

### getDiscoveryRunInferredKind(*run_id*, *inferred_kind* [, offset=*optional* ] [, results_id=*optional* ] [, format=*optional* ]):

| Parameters | Type | Use | Options
| - | - | - | -
| **run_id** | String | Required | |
| **inferred_kind** | String | Required | |
| offset=**intger** | Integer | | |
| results_id=**string** | String | | |
| format=**string** | String | | "object"

- Get a summary of the devices inferred by a discovery run which have a specific inferred kind.

```python
>>> tw.getDiscoveryRunResult("1234567890", "Host", format="object").json()
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
>>> td = tideway.data('appliance-hostname','auth-token')
```

### search(*query* [, offset=*optional* ] [, results_id=*optional* ] [, format=*optional* ])

| Parameters | Type | Use | Options
| - | - | - | -
| **query** | String | Required | |
| offset=**intger** | Integer | | |
| results_id=**string** | String | | |
| format=**string** | String | | "object"

- Run a search query, receiving paginated results.

```python
>>> td.search("search Host show os_type process with unique()").json()
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

### searchQuery(*json* [, offset=*optional* ] [, results_id=*optional* ] [, format=*optional* ])

| Parameters | Type | Use | Options
| - | - | - | -
| **json** | JSON | Required | {"query":"search string"}
| offset=**intger** | Integer | | |
| results_id=**string** | String | | |
| format=**string** | String | | "object"

- An alternative to GET /data/search, for search queries which are too long for urls.

```python
>>> td.searchQuery({"query": "search Host show os_class process with unique()"}, format="object").json()
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

### nodeLookup(*node_id* [, relationships=*optional* (default=*False*) ] [, traverse=*optional* ] [, flags=*optional* ])

| Parameters | Type | Use | Options
| - | - | - | -
| **node_id** | JSON | Required | |
| relationships=**boolean** | String | | True<br>False
| traverse=**string** | String | | "NodeKind:Relationship:NodeKind:Node"
| flags=**string** | String | | "include_destroyed"<br>"exclude_current" |

- Get the state of a node with specified id.

```python
>>> td.nodeLookup("a1b2c3d4e5f6")
```

### lookupNodeKind(*kind* [, offset=*optional* ] [, results_id=*optional* ] [, format=*optional* ])

| Parameters | Type | Use | Options
| - | - | - | -
| **kind** | String | Required | |
| offset=**intger** | Integer | | |
| results_id=**string** | String | | |
| format=**string** | String | | "object"

- Finds all nodes of a specified node kind.

```python
>>> td.lookupNodeKind("Host")
```

### graphNode(*node_id* [, focus=*optional* (default=*"sofware-connected"*)] [, apply_rules=*optional* (default=*True*) ])

| Parameters | Type | Use | Options
| - | - | - | -
| **node_id** | JSON | Required | |
| focus=**string** | String | | "software-connected"<br>"software"<br>"infrastructure"
| apply_rules=**boolean** | Boolean | | True<br>False

- Graph data represents a set of nodes and relationships that are associated to the given node.

```python
>>> td.graphNode("a1b2c3d4e5f6")
```

## Vault

- Initiate a Vault object for the instance of Discovery you intend to manage.

```python
>>> import tideway
>>> tv = tideway.vault('appliance-hostname','auth-token')
```

### getVault()

- Get details of the state of the vault.

```python
>>> tv.getVault().json()
{'open': True, 'passphrase_saved': False, 'passphrase_set': False}
```

### updateVault(*json*)

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required

- Change the state of the vault.

```python
>>> tv.updateVault({"open": True,"passphrase": "pass phrase"})
```

## Credentials

- Initiate a Credential object for the instance of Discovery you intend to query.

```python
>>> import tideway
>>> tc = tideway.credentials('appliance-hostname','auth-token')
```

### listCredentialTypes([ group=*optional* ] [, category=*optional* ])

| Parameters | Type
| - | -
| group=**string** | String
| category=**string** | String

- Get a list of all credential types and filter by group and/or category.

```python
>>> tc.listCredentialTypes(category="Database").json()
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

### credentialType(*cred_type_name*)

| Parameters | Type | Use
| - | - | -
| **cred_type_name** | String | Required

- Get the properties of a specific credential type.

```python
>>> tc.credentialType("oracle").json()
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

### listCredentials([cred_id=*optional*])

| Parameters | Type
| - | -
| cred_id=**string** | String

- Get a list of credentials.

```python
>>> tc.listCredentials()
```

### newCredential(*json*)

| Parameters | Type | Use
| - | - | -
| **json** | String | Required

- Create a new credential.

```python
>>> tc.newCredential({
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

### deleteCredential(*cred_id*)

| Parameters | Type | Use
| - | - | -
| cred_id=**string** | String | Required

- Delete a credential.

```python
>>> tc.deleteCredential("a1b2c3d4e5f6").ok
True
```

### updateCredential(*cred_id*, *json*)

| Parameters | Type | Use
| - | - | -
| cred_id=**string** | String | Required
| **json** | String | Required

- Updates partial resources of a credential. Missing properties are left unchanged.

```python
>>> tc.updateCredential("a1b2c3d4e5f6",{ "enabled" : False }).ok
True
```

### replaceCredential(*cred_id*, *json*)

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
>>> tk = tideway.knowledge('appliance-hostname','auth-token')
```

### getKnowledgeManagement()

- Get the current state of the appliance's knowledge, including TKU versions.

```python
>>> tk.getKnowledgeManagement().json()
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

### getUploadStatus()

- Get the current state of a knowledge upload.

```python
>>> tk.getUploadStatus().json()
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

### uploadKnowledge(*filename*, *file* [, activate=*optional* (default=*True*) ] [, allow_restart=*optional* (default=*False*)])

| Parameters | Type | Use | Options
| - | - | - | -
| **filename** | String | Required | |
| **file** | String | Required | |
| activate=**boolean** | Boolean | | True<br>False |
| allow_restart=**boolean** | Boolean | | True<br>False |

- Upload a TKU or pattern module to the appliance.

```python
>>> tk.uploadKnowledge("TestPattern.tpl","C:/Users/User001/Documents/TestPattern.tpl")
```

## Events

- Initiate an Event object for the instance of Discovery you intend to query.

```python
>>> import tideway
>>> te = tideway.events('appliance-hostname','auth-token')
```

### status(*json*)

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required |

- Returns a unique ID if the event has been recorded, otherwise an empty string is returned e.g. if the event source has been disabled.

```python
>>> te.status({"source":"Event1","type":"EventType1"}
})
```

## Admin

- Initiate an Admin object for the instance of Discovery you intend to query.

```python
>>> import tideway
>>> ta = tideway.admin('appliance-hostname','auth-token')
```

### baseline()

- Get a summary of the appliance status, and details of which baseline checks have passed or failed.

```python
>>> ta.baseline().json()
{
    "results": {
        "FAILED": [
            {
                "enabled": true,
                "message": "MAJOR: This appliance has insufficent resources",
                "name": "Appliance Specification",
                "severity": "MAJOR"
            },
            {
                "details": [
                    {
                        "messages": [
                            "2 credentials have been added",
...
```

### about()

- Get information about the appliance, like its version and versions of the installed packages.

```python
>>> ta.about()
{
    "versions": {
        "devices": "5.0.2020.09.3",
        "os_updates": "7.20.08.25",
        "product": "12.1",
        "product_content": "2.0.2020.09.3"
    }
}
```

### licensing([ content_type=*optional* (default="text/plain") ])

| Parameters | Type | Use | Options
| - | - | - | -
| content_type=**string** | String | | "text/plain"<br>"csv"<br>"raw" |

- Get the latest signed licensing report.
- CSV option returns raw license data in CSV format as a zip file for offline analysis.
- RAW option return an encrypted raw license object for import to another appliance.

```python
>>> ta.licensing()
-----BEGIN LICENSE REPORT-----
License report
==============

Report start time: 2021-01-18 23:00:00.409987+00:00
Report end time  : 2021-01-21 23:00:00.410085+00:00
...
```
