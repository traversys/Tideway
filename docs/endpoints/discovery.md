---
sort: 2
---

# Discovery

Initiate a Discovery object for the instance of Discovery you intend to query.

Syntax:

<pre>**tideway.discovery(**__target__, __token__ [, _api_version_ ] [, _ssl_verify_ ] [, _limit_ ] [, _offset_ ]**)**</pre>

Initiation:
```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> discovery = tw.discovery()
```

## getDiscoveryStatus()

Get the current status of the discovery process.

Syntax:

<pre>**.getDiscoveryStatus()**</pre>

Example:
```python
>>> >>> discovery.getDiscoveryStatus().json()
{'running': False, 'status': 'running'}
```

## setDiscoveryStatus()

Start or stop the discovery process.

Syntax:

<pre>**setDiscoveryStatus(__json__)**</pre>

| Parameters   | Type        | Required | Default Value | Options |
| ------------ | ----------- | :------: | ------------- | --------|
| json         | JSON Object | Yes      | N/A           | N/A     |

Example:
```python
>>> >>> discovery.getDiscoveryStatus().json()
{'running': False, 'status': 'stopped'}
>>> discovery.setDiscoveryStatus({"status": "running"}).ok
True
>>> >>> discovery.getDiscoveryStatus().json()
{'running': False, 'status': 'running'}
```

## getApiProviderMetadata()

Get metadata for the API providers currently supported by BMC Discovery.

Syntax:

<pre>**.getApiProviderMetadata()**</pre>

```python
>>> discovery.getApiProviderMetadata().json()[0]['cred_params'][0]
{'allowed_values': [], 'description': 'URL of the Kubernetes/OpenShift cluster with port', 'is_list': False, 'mandatory': False, 'name': 'kubernetes.cluster_url', 'type': 'str'}
```

## getDiscoveryCloudMetaData()

Get metadata for the cloud providers currently supported by BMC Discovery.

Syntax:

<pre>**.getDiscoveryCloudMetaData()**</pre>

```python
discovery.getDiscoveryCloudMetaData().json()[0]['cred_params'][0]
{'allowed_values': [], 'description': 'Azure Directory ID (also known as the Tenant ID)', 'is_list': False, 'mandatory': True, 'name': 'azure.tenant_id', 'type': 'str'}
```

## discoveryRun()

Create a new snapshot discovery run.

Syntax:

<pre>**.discoveryRun(__json__)**</pre>

| Parameters   | Type        | Required | Default Value | Options |
| ------------ | ----------- | :------: | ------------- | --------|
| json         | JSON Object | Yes      | N/A           | N/A     |

Example:
```python
>>> discovery.discoveryRun({"ranges":[ "192.168.1.0/24" ],"label":"Network Snapshot","scan_level":"Full Discovery"}).ok
True
```
## getDiscoveryRuns()

Get details of all currently processing discovery runs.

Syntax:

<pre>**.getDiscoveryRuns()**</pre>

Example:
```python
>>> discovery.getDiscoveryRuns().json()
[]
```

## getDiscoveryRun()

Get details of specific currently processing discovery run.

Syntax:

<pre>**.getDiscoveryRun(__run_id__)**</pre>

| Parameters   | Type   | Required | Default Value | Options |
| ------------ | ------ | :------: | ------------- | --------|
| run_id       | String | Yes      | N/A           | N/A     |

Example:
```python
>>> run = discovery.getDiscoveryRun("1234567890")
>>> from pprint import pprint
>>> pprint(run.json())
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

## updateDiscoveryRun()

Update the state of a specific discovery run.

Syntax:

<pre>**.updateDiscoveryRun(__run_id__, __json__)**</pre>

| Parameters   | Type        | Required | Default Value | Options |
| ------------ | ----------- | :------: | ------------- | --------|
| run_id       | String      | Yes      | N/A           | N/A     |
| json         | JSON Object | Yes      | N/A           | N/A     |

Example:
```python
>>> discovery.updateDiscoveryRun("1234567890", {"cancelled": True}).ok
True
```

## getDiscoveryRunResults()

Get a summary of the results from scanning all endpoints in the run, partitioned by result type.

Syntax:

<pre>**.getDiscoveryRunResults(__run_id__)**</pre>

| Parameters   | Type        | Required | Default Value | Options |
| ------------ | ----------- | :------: | ------------- | --------|
| run_id       | String      | Yes      | N/A           | N/A     |

Example:
```python
>>> run = discovery.getDiscoveryRunResults("1234567890")
>>> print(run.text)
{
    "Dropped": {
        "count": 204,
        "uri": "https://appliance/api/v1.2/discovery/runs/1234567890/results/Dropped"
    },
    "Skipped": {
        "count": 3,
        "uri": "https://appliance/api/v1.2/discovery/runs/1234567890/results/Skipped"
    },
    "Success": {
        "count": 47,
        "uri": "https://appliance/api/v1.2/discovery/runs/1234567890/results/Success"
    }
}
```

## getDiscoveryRunResult()

Get a summary of the results from scanning all endpoints in the run that had a specific type of result.

Syntax:

<pre>**.getDiscoveryRunResult(**__run_id__ [, result ] [, offset ] [, results_id ] [, format ] [, limit ] [, delete ]**)**</pre>

| Parameters   | Type        | Required | Default Value | Options  |
| ------------ | ----------- | :------: | ------------- | -------- |
| run_id       | String      | Yes      | N/A           | N/A      |
| result       | String      | No       | "Success"     | <ul><li>"Success"</li><li>"Skipped"</li><li>"NoAccess"</li><li>"NoResponse"</li><li>"Error"</li><li>"Dropped"</li></ul> |
| offset       | Integer     | No       | N/A           | N/A      |
| results_id   | String      | No       | N/A           | N/A      |
| format       | String      | No       | N/A           | <ul><li>"object"</li></ul> |
| limit        | Integer     | No       | 100           | N/A      |
| delete       | Boolean     | No       | False         | <ul><li>True</li><li>False</li></ul> |

Example: Retrieve DiscoveryRuns which ended with an Error, and retrieve result rows 51-100.
```python
>>> discovery.getDiscoveryRunResult("1234567890", result="Error", offset=50, results_id="a12b3cd4e5f6", limit=50)
```
## getDiscoveryRunInferred()

Get a summary of all inferred devices from a discovery run, partitioned by device type.

Syntax:

<pre>**.getDiscoveryRunInferred(__run_id__)**</pre>

| Parameters   | Type        | Required | Default Value | Options  |
| ------------ | ----------- | :------: | ------------- | -------- |
| run_id       | String      | Yes      | N/A           | N/A      |

Example:
```python
>>> discovery.getDiscoveryRunInferred("1234567890")
```

## getDiscoveryRunInferredKind()

Get a summary of the devices inferred by a discovery run which have a specific inferred kind.

Syntax:

<pre>**.getDiscoveryRunInferredKind(**__run_id__ , __inferred_kind__ [, offset ] [, results_id ] [, format ] [, limit ] [, delete ]**)**</pre>

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| run_id        | String      | Yes      | N/A           | N/A      |
| inferred_kind | String      | Yes      | N/A           | N/A      |
| offset        | Integer     | No       | N/A           | N/A      |
| results_id    | String      | No       | N/A           | N/A      |
| format        | String      | No       | N/A           | <ul><li>"object"</li></ul> |
| limit         | Integer     | No       | 100           | N/A      |
| delete        | Boolean     | No       | False         | <ul><li>True</li><li>False</li></ul> |

Example:
```python
>>> result = discovery.getDiscoveryRunResult("1234567890", "Host", format="object")
>>> print(result.text)
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