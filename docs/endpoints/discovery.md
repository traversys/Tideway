---
sort: 3
---

# Discovery

- Initiate a Discovery object for the instance of Discovery you intend to query.

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> discovery = tw.discovery()
```

## getDiscoveryStatus()

- Get the current status of the discovery process.

```python
>>> status = discovery.getDiscoveryStatus()
>>> status.json()
{
	'running': False,
	'status': 'running'
}
```

## setDiscoveryStatus(*json*)

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required

- Start or stop the discovery process.

```python
>>> discovery.setDiscoveryStatus({"status": "running"}).ok
True
```

## getApiProviderMetadata()

- Get metadata for the API providers currently supported by BMC Discovery.

```python
>>> discovery.getApiProviderMetadata()
```

## getDiscoveryCloudMetaData()

- Get metadata for the cloud providers currently supported by BMC Discovery.

```python
>>> discovery.getDiscoveryCloudMetaData()
```

## discoveryRun(*json*)

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
## getDiscoveryRuns()

- Get details of all currently processing discovery runs.

```python
>>> discovery.getDiscoveryRuns()
```
## getDiscoveryRun(*run_id*)

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
## updateDiscoveryRun(*run_id*, *json*)

| Parameters | Type | Use
| - | - | -
| **run_id** | String | Required
| **json** | JSON | Required

- Update the state of a specific discovery run.

```python
>>> discovery.updateDiscoveryRun("1234567890", {"cancelled": True}).ok
True
```
## getDiscoveryRunResults(*run_id*)

| Parameters | Type | Use
| - | - | -
| **run_id** | String | Required

- Get a summary of the results from scanning all endpoints in the run, partitioned by result type.

```python
>>> discovery.getDiscoveryRunResults("1234567890")
```
## getDiscoveryRunResult(*run_id* [, result=*optional* (default=*"Success"*) ] [, offset=*optional* ] [, results_id=*optional* ] [, format=*optional* ] [, limit=*optional*] [, delete=*optional*])

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
## getDiscoveryRunInferred(*run_id*)

| Parameters | Type | Use
| - | - | -
| **run_id** | String | Required

- Get a summary of all inferred devices from a discovery run, partitioned by device type.

```python
>>> discovery.getDiscoveryRunInferred("1234567890")
```
## getDiscoveryRunInferredKind(*run_id*, *inferred_kind* [, offset=*optional* ] [, results_id=*optional* ] [, format=*optional* ] [, limit=*optional*] [, delete=*optional*])

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