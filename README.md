# Tideway

Simplified Python library for BMC Discovery API Interface that makes use of the Python Requests module (https://github.com/psf/requests) and uses the response handler.

```python
>>> import tideway
>>> tw = tideway.admin('appliance-hostname','auth-token')
>>> tw.about().url
'https://appliance-hostname/api/v1.1/admin/about'
>>> tw.about().status_code
200
>>> tw.about().json()
{'versions': {'devices': '5.0.2020.09.3', 'os_updates': '7.20.08.25', 'product': '12.1', 'product_content': '2.0.2020.09.3'}}
```

Tideway follows BMC Disocery's well-structured and documented REST API which can be viewed from `https://<appliance>/swagger-ui/`.

Tideway removes the extra layer of manually construting a URL and parameters for python requests allowing you to query API supported features of Discovery seamlessly and faster than if you were to navigate via the GUI.

## Installing Requests and Supported Versions

- Tideway can be installed via PyPI:

```console
$ python -m pip install tideway
```

- Tideway supports BMC Discovery 11.3+, API v1.1 using Python 3.

## Quickstart Guide

### Discovery

- Initiate a Discovery object for the instance of Discovery you intend to query.

```python
>>> import tideway
>>> tw = tideway.discovery('appliance-hostname','auth-token')
```

You can specify the following optional parameters:

| Parameter | Type | Default | Description
| - | - | - | -
| limit | Integer | 100 | This limits the amount of results returned by the API. You can use optional offset parameters on some queries in order to retrieve results in batches.
| delete | Boolean | False | If supported, you can speficy to delete the results of a function call.

#### getDiscoveryStatus()

- Get the current status of the discovery process.

```python
>>> status = tw.getDiscoveryStatus()
>>> status.json()
{'running': False, 'status': 'running'}
```

#### setDiscoveryStatus(*json*)

- Start or stop the discovery process.

```python
>>> tw.setDiscoveryStatus({"status": "running"}).ok
True
```

#### getDiscoveryCloudMetaData()

- Get metadata for the cloud providers currently supported by BMC Discovery.

#### discoveryRun(*json*)

- Create a new snapshot discovery run.

```python
>>> tw.discoveryRun({
  "ranges": [ "192.168.1.0/24" ],
  "label": "Network Snapshot",
  "scan_level": "Full Discovery"
}).ok
True
```

#### getDiscoveryRuns()

- Get details of all currently processing discovery runs.

#### getDiscoveryRun(*run_id*)

- Get details of specific currently processing discovery run.

```python
>>> tw.getDiscoveryRun("1234567890").json()
[{'label': 'Network Snapshot', 'scan_kind': 'IP', 'scan_level': 'Full Discovery', 'scan_type': 'Snapshot', 'total': 254, 'valid_ranges': '192.168.1.0/24', uuid:'1234567890'}]
```

#### updateDiscoveryRun(*run_id*, *json*)

- Update the state of a specific discovery run.

```python
>>> tw.updateDiscoveryRun("1234567890", {"cancelled": True}).ok
True
```

#### getDiscoveryRunResults(*run_id*)

- Get a summary of the results from scanning all endpoints in the run, partitioned by result type.

#### getDiscoveryRunResult(*run_id* [, result=*optional* (default=*"Success"*) ] [, offset=*optional* ] [, results_id=*optional* ] [, format=*optional* ])

- Get a summary of the results from scanning all endpoints in the run that had a specific type of result.
- Example: Retrieve DiscoveryRuns which ended with an Error, and retrieve result rows 51-100.

```python
>>> tw = tideway.discovery('appliance-hostname','auth-token',limit=50)
>>> tw.getDiscoveryRunResult("1234567890", result="Error", offset=50, results_id="a12b3cd4e5f6")
```

#### getDiscoveryRunInferred(*run_id*)

- Get a summary of all inferred devices from a discovery run, partitioned by device type.

#### getDiscoveryRunInferredKind(*run_id*, *inferred_kind* [, offset=*optional* ] [, results_id=*optional* ] [, format=*optional* ]):

- Get a summary of the devices inferred by a discovery run which have a specific inferred kind.

```python
>>> tw.getDiscoveryRunResult("1234567890", "Host", format="object").json()
[{'count': 4, 'kind': 'Host', 'offset': 0, 'results': [{'#InferredElement:Inference:Associate:DiscoveryAccess.endpoint': ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.10'], '#id': 'a12b3cd4e5f6'...
```

### Data

- Initiate a Data object for the instance of Discovery you intend to query.

```python
>>> import tideway
>>> td = tideway.data('appliance-hostname','auth-token')
```

- You can specify the following optional parameters:

| Parameter | Type | Default | Description
| - | - | - | -
| limit | Integer | 100 | This limits the amount of results returned by the API. You can use optional offset parameters on some queries in order to retrieve results in batches.
| delete | Boolean | False | If supported, you can speficy to delete the results of a function call.

#### search(*query* [, offset=*optional* ] [, results_id=*optional* ] [, format=*optional* ])

- Run a search query, receiving paginated results.

```python
>>> td.search("search Host show os_type process with unique()").json()
[{'count': 12, 'headings': ['os_type'], 'kind': 'Unique row', 'offset': 0, 'results': [['Ubuntu Linux'], ['Windows'], ['CentOS Linux'], ['GNU/Linux'], ['Red Hat Enterprise Linux'], ['Amazon Linux AMI'], ['Solaris'], ['SuSE Linux'], ['AIX'], ['FreeBSD'], ['VMware ESXi'], ['HP-UX']]}]
```

#### searchQuery(*json* [, offset=*optional* ] [, results_id=*optional* ] [, format=*optional* ])

- An alternative to GET /data/search, for search queries which are too long for urls.

```python
>>> td.searchQuery({"query": "search Host show os_class process with unique()"}, format="object").json()
[{'count': 3, 'kind': 'Unique row', 'offset': 0, 'results': [{'os_class': 'UNIX'}, {'os_class': 'Windows'}, {'os_class': 'Other'}]}]
```

#### nodeLookup(*node_id* [, relationships=*optional* (default=*False*) ] [, traverse=*optional* ] [, flags=*optional*])

- Get the state of a node with specified id.

#### lookupNodeKind(*kind*, [, offset=*optional* ] [, results_id=*optional* ] [, format=*optional* ])

- Finds all nodes of a specified node kind.

#### graphNode(*node_id* [, focus=*optional* (default=*"sofware-connected"*)] [, apply_rules=*optional* (default=*True*) ])

- Graph data represents a set of nodes and relationships that are associated to the given node.

### Vault

- Initiate a Vault object for the instance of Discovery you intend to manage.

```python
>>> import tideway
>>> tv = tideway.vault('appliance-hostname','auth-token')
```

#### getVault()

- Get details of the state of the vault.

```python
>>> tv.getVault().json()
{'open': True, 'passphrase_saved': False, 'passphrase_set': False}
```

#### updateVault(*json*)

- Change the state of the vault.
