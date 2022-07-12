---
sort: 5
---

# Discovery

Initiate a Discovery object for the instance of Discovery you intend to query.

Syntax:

```
tideway.discovery(__target__, __token__ [, _api_version_ ] [, _ssl_verify_ ] [, _limit_ ] [, _offset_ ])
```

Initiation:

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> discovery = tw.discovery()
```

## get_discovery

Get the current status of the discovery process.

Syntax:

```
.get_discovery
```

Example:
```python
>>> >>> discovery.get_discovery.json()
{'running': False, 'status': 'running'}
```

## patch_discovery()

Start or stop the discovery process.

Syntax:

```
.patch_discovery(__json__)
```

| Parameters   | Type        | Required | Default Value | Options |
| ------------ | ----------- | :------: | ------------- | --------|
| json         | JSON Object | Yes      | N/A           | N/A     |

Example:

```python
>>> >>> discovery.get_discovery.json()
{'running': False, 'status': 'stopped'}
>>> discovery.patch_discovery({"status": "running"}).ok
True
>>> >>> discovery.get_discovery.json()
{'running': False, 'status': 'running'}
```

## get_discovery_api_provider_metadata

Get metadata for the API providers currently supported by BMC Discovery.

Syntax:

```
.get_discovery_api_provider_metadata
```

```python
>>> discovery.get_discovery_api_provider_metadata.json()[0]['cred_params'][0]
{'allowed_values': [], 'description': 'URL of the Kubernetes/OpenShift cluster with port', 'is_list': False, 'mandatory': False, 'name': 'kubernetes.cluster_url', 'type': 'str'}
```

## get_discovery_api_cloud_metadata

Get metadata for the cloud providers currently supported by BMC Discovery.

Syntax:

```
.get_discovery_api_cloud_metadata
```

```python
discovery.get_discovery_api_cloud_metadata.json()[0]['cred_params'][0]
{'allowed_values': [], 'description': 'Azure Directory ID (also known as the Tenant ID)', 'is_list': False, 'mandatory': True, 'name': 'azure.tenant_id', 'type': 'str'}
```

## getDiscoveryStatus()

[Deprecated] See [get_discovery](#get_discovery) for usage.

Syntax: `.getDiscoveryStatus()`

## setDiscoveryStatus()

[Deprecated] See [patch_discovery](#patch_discovery) for usage.

Syntax: `.setDiscoveryStatus(__json__)`

## getApiProviderMetadata()

[Deprecated] See [get_discovery_api_provider_metadata](#get_discovery_api_provider_metadata) for usage.

Syntax: `.getApiProviderMetadata()`

## getDiscoveryCloudMetaData()

[Deprecated] See [get_discovery_api_cloud_metadata](#get_discovery_api_cloud_metadata) for usage.

Syntax: `.getDiscoveryCloudMetaData()`

## get_discovery_exclude()

Get a list of all or specific excludes.

Syntax:

```
.get_discovery_exclude([ _exclude_id_ ])
```

| Parameters   | Type        | Required | Default Value | Options |
| ------------ | ----------- | :------: | ------------- | --------|
| exclude_id   | String      | No       | N/A           | N/A     |

## get_discovery_excludes

Get a list of all excludes. See [get_discovery_exclude](#get_discovery_exclude).

Syntax: `.get_discovery_excludes`

## post_discovery_exclude()

Update an exclude list.

Syntax:

```
.post_discovery_exclude(__json__)
```

| Parameters   | Type        | Required | Default Value | Options |
| ------------ | ----------- | :------: | ------------- | --------|
| json         | JSON Object | Yes      | N/A           | N/A     |

## delete_discovery_exclude()

Delete an exclude list.

Syntax:

```
.delete_discovery_exclude(__exclude_id__)
```

| Parameters   | Type        | Required | Default Value | Options |
| ------------ | ----------- | :------: | ------------- | --------|
| exclude_id   | String      | Yes      | N/A           | N/A     |

## patch_discovery_exclude()

Update an exclude list.

Syntax:

```
.patch_discovery_exclude(__json__, __exclude_id__)
```

| Parameters   | Type        | Required | Default Value | Options |
| ------------ | ----------- | :------: | ------------- | --------|
| json         | JSON Object | Yes      | N/A           | N/A     |
| exclude_id   | String      | Yes      | N/A           | N/A     |

## get_discovery_run()

Get details of specific currently processing discovery run.

Syntax:

```
.get_discovery_run(__run_id__)
```

| Parameters   | Type   | Required | Default Value | Options |
| ------------ | ------ | :------: | ------------- | --------|
| run_id       | String | Yes      | N/A           | N/A     |

Example:
```python
>>> run = discovery.get_discovery_run("1234567890")
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

## get_discovery_runs

Get details of all currently processing discovery runs. See [get_discovery_run](#get_discovery_run).

Syntax: `.get_discovery_runs`

## post_discovery_run()

Create a new snapshot discovery run.

Syntax:

```
.post_discovery_run(__json__)
```

| Parameters   | Type        | Required | Default Value | Options |
| ------------ | ----------- | :------: | ------------- | --------|
| json         | JSON Object | Yes      | N/A           | N/A     |

Example:
```python
>>> discovery.post_discovery_run({"ranges":[ "192.168.1.0/24" ],"label":"Network Snapshot","scan_level":"Full Discovery"}).ok
True
```

## patch_discovery_run()

Update the state of a specific discovery run.

Syntax:

```
.patch_discovery_run(__run_id__, __json__)
```

| Parameters   | Type        | Required | Default Value | Options |
| ------------ | ----------- | :------: | ------------- | --------|
| run_id       | String      | Yes      | N/A           | N/A     |
| json         | JSON Object | Yes      | N/A           | N/A     |

Example:
```python
>>> discovery.patch_discovery_run("1234567890", {"cancelled": True}).ok
True
```

## getDiscoveryRun()

[Deprecated] See [get_discovery_run](#get_discovery_run) for usage.

Syntax: `.getDiscoveryRun(__run_id__)`

## getDiscoveryRuns()

[Deprecated] See [get_discovery_runs](#get_discovery_runs) for usage.

Syntax: `.getDiscoveryRuns()`

## discoveryRun()

[Deprecated] See [post_discovery_run](#post_discovery_run) for usage.

Syntax: `.discoveryRun(__json__)`

## updateDiscoveryRun()

[Deprecated] See [patch_discovery_run](#patch_discovery_run) for usage.

Syntax: `.updateDiscoveryRun(__run_id__, __json__)`

## get_discovery_run_results()

Get a summary of the results from scanning all endpoints in the run, partitioned by result type that had a specific type of result.

Syntax:

```
.get_discovery_run_results(__run_id__ [, result ] [, offset ] [, results_id ] [, format ] [, limit ] [, delete ])
```

| Parameters   | Type        | Required | Default Value | Options  |
| ------------ | ----------- | :------: | ------------- | -------- |
| run_id       | String      | Yes      | N/A           | N/A      |
| result       | String      | No       | "Success"     | <ul><li>"Success"</li><li>"Skipped"</li><li>"NoAccess"</li><li>"NoResponse"</li><li>"Error"</li><li>"Dropped"</li></ul> |
| offset       | Integer     | No       | N/A           | N/A      |
| results_id   | String      | No       | N/A           | N/A      |
| format       | String      | No       | N/A           | <ul><li>"object"</li></ul> |
| limit        | Integer     | No       | 100           | N/A      |
| delete       | Boolean     | No       | False         | <ul><li>True</li><li>False</li></ul> |

Example:
```python
>>> run = discovery.get_discovery_run_results("1234567890")
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

## getDiscoveryRunResults()

[Deprecated] See [get_discovery_run_results](#get_discovery_run_results) for usage.

Syntax: `.getDiscoveryRunResults(__run_id__)`

## getDiscoveryRunResult()

[Deprecated] See [get_discovery_run_results](#get_discovery_run_results) for usage.

Syntax: `.getDiscoveryRunResults(__run_id__, __result__ [, offset ] [, results_id ] [, format ] [, limit ] [, delete ])`

## get_discovery_run_inferred()

Get a summary of all inferred devices from a discovery run, partitioned by device type and/or which have a specific inferred kind.

Syntax:

```
.get_discovery_run_inferred(__run_id__ [, inferred_kind ] [, offset ] [, results_id ] [, format ] [, limit ] [, delete ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| run_id        | String      | Yes      | N/A           | N/A      |
| inferred_kind | String      | No       | N/A           | N/A      |
| offset        | Integer     | No       | N/A           | N/A      |
| results_id    | String      | No       | N/A           | N/A      |
| format        | String      | No       | N/A           | <ul><li>"object"</li></ul> |
| limit         | Integer     | No       | 100           | N/A      |
| delete        | Boolean     | No       | False         | <ul><li>True</li><li>False</li></ul> |

Example:
```python
>>> result = discovery.get_discovery_run_inferred("1234567890", "Host", format="object")
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

## getDiscoveryRunInferred()

[Deprecated] See [get_discovery_run_inferred](#get_discovery_run_inferred) for usage.

Syntax: `.getDiscoveryRunInferred(__run_id__)`

## getDiscoveryRunInferredKind()

[Deprecated] See [get_discovery_run_inferred](#get_discovery_run_inferred) for usage.

Syntax: `.getDiscoveryRunInferredKind(__run_id__ , __inferred_kind__ [, offset ] [, results_id ] [, format ] [, limit ] [, delete ])`

## get_discovery_run_schedule()

Get a list of all or specific scan schedules.

Syntax:

```
.get_discovery_run_schedule([ _run_id_ ])
```

| Parameters   | Type        | Required | Default Value | Options |
| ------------ | ----------- | :------: | ------------- | --------|
| run_id       | String      | No       | N/A           | N/A     |

## get_discovery_run_schedules()

Get a list of all or specific scan schedules. See [get_discovery_run_schedule](#get_discovery_run_schedule).

Syntax: `.get_discovery_run_schedules`

## post_discovery_run_schedule()

Add a new scan schedule.

Syntax:

```
.post_discovery_run_schedule(__json__)
```

| Parameters   | Type        | Required | Default Value | Options |
| ------------ | ----------- | :------: | ------------- | --------|
| json         | JSON Object | Yes      | N/A           | N/A     |

## delete_discovery_run_schedule()

Delete a specific scan schedule.

Syntax:

```
.delete_discovery_run_schedule(__run_id__)
```

| Parameters   | Type        | Required | Default Value | Options |
| ------------ | ----------- | :------: | ------------- | --------|
| run_id       | String      | Yes      | N/A           | N/A     |

## patch_discovery_run_schedule()

Update a specific scan schedule.

Syntax:

```
.patch_discovery_run_schedule(__run_id__, __json__)
```

| Parameters   | Type        | Required | Default Value | Options |
| ------------ | ----------- | :------: | ------------- | --------|
| run_id       | String      | Yes      | N/A           | N/A     |
| json         | JSON Object | Yes      | N/A           | N/A     |