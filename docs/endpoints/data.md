---
sort: 4
---

# Data

Initiate a Data object for the instance of Discovery you intend to query.

Syntax:

```
tideway.data(__target__, __token__ [, _api_version_ ] [, _ssl_verify_ ] [, _limit_ ] [, _offset_ ])
```

Initiation:

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> data = tw.data()
```

## get_data_search()

Default search. See [search](#search) for usage.

## post_data_search()

Alternative search method. See [search](#search) for usage.

## get_data_search_object()

Search defaulted to 'object' format. See [search](#search) for usage.

## post_data_search_object()

Alternative search method defaulted to 'object' format. See [search](#search) for usage.

## get_data_search_tree()

Search defaulted to 'tree' format. See [search](#search) for usage.

## post_data_search_tree()

Alternative search method defaulted to 'tree' format. See [search](#search) for usage.

## search()

Run a search query, receiving paginated results.

Syntax:

```
.search(__query__ [, _offset_ ] [, _results_id_ ] [, _format_ ] [, _limit_ ] [, _delete_ ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| query | <ul><li>String</li><li>JSON Object</li></ul> | Yes | N/A | N/A |
| offset        | Integer     | No       | N/A           | N/A      |
| results_id    | String      | No       | N/A           | N/A      |
| format        | String      | No       | N/A           | <ul><li>"object"</li><li>"tree"</li></ul> |
| limit         | Integer     | No       | 100           | N/A      |
| delete        | Boolean     | No       | False         | <ul><li>True</li><li>False</li></ul> |

Example:

```python
>>> search = data.search("search Host show os_type process with unique()")
>>> print(search.json())
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

## search_bulk()

Run a search bulk search query, will loop paginated results and return all results as a JSON list object. The function makes use of results_id and offset automatically so these are not required as arguments.

```note
This function may take a long time to run as it will be run multiple API calls until the entire query is fulfilled.
```

Syntax:

```
.search_bulk(__query__ [, _format_ ] [, _limit_ ] [, _delete_ ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| query | <ul><li>String</li><li>JSON Object</li></ul> | Yes | N/A | <ul><li>"search string"</li><li>{"query":"search string"}</li></ul> |
| format        | String      | No       | N/A           | <ul><li>"object"</li><li>"tree"</li></ul> |
| limit         | Integer     | No       | 100           | N/A      |
| delete        | Boolean     | No       | False         | <ul><li>True</li><li>False</li></ul> |

Example: This search_bulk() returns 500 results each time, and makes 2 additional API calls
```python
>>> search_results = data.search_bulk("search Host show name", limit=500)
>>> print(len(search_results))
1510
```

## post_data_condition()

Search using a condition, return tabular results as arrays.

Syntax:

```
.post_data_condition(__body__ [, _offset_ ] [, _results_id_ ] [, _format_ ] [, _limit_ ] [, _delete_ ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| body          | JSON Object | Yes      | N/A           | N/A      |
| offset        | Integer     | No       | N/A           | N/A      |
| results_id    | String      | No       | N/A           | N/A      |
| format        | String      | No       | N/A           | <ul><li>"object"</li><li>"tree"</li></ul> |
| limit         | Integer     | No       | 100           | N/A      |
| delete        | Boolean     | No       | False         | <ul><li>True</li><li>False</li></ul> |

## post_data_condition_param_values()

Get possible parameter values for a condition.

Syntax:

```
.post_data_condition_param_values(__body__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| body          | JSON Object | Yes      | N/A           | N/A      |

## get_data_condition_params()

Retrieve the list of available condition parameters.

Syntax:

```
.get_data_condition_params
```

## get_data_condition_template()


Get the properties of a specific template or a list of all templates.

Syntax:

```
.get_data_condition_template([ _template_id_ ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| template_id   | String      | No       | N/A           | N/A      |

Example:

```python
>>> templates = data.get_data_condition_template()
>>> print(templates.text)
[]
```

## get_data_condition_templates

Get a list of all available templates. See [get_data_condition_template](#get_data_condition_template).

## post_data_candidate()

The node object of the best candidate based on the provided parameters.

Syntax:

```
.post_data_candidate(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |

Example:

```python
>>> candidates = data.post_data_candidate({"hostname": "disco","kind" : "Host"})
>>> print(candates.text)
{
  "#id": "30c577625e064d10300b17ea6e486f7374",
  "__all_dns_names": [
    "disco.local"
  ],
  "__all_ip_addrs": [
    "10.16.15.99",
    "fe80::4bcc:a31c:43a:c258"
  ],
  "__all_mac_addrs": [
    "02:11:32:23:29:f0"
  ],
...
```

## post_data_candidates()

Enter parameters to identify a device, the response is a list of candidate nodes ordered by descending score.

Syntax:

```
.post_data_candidates(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |

## get_data_nodes()

Get the state of a node with specified id.

Syntax:

```
.get_data_nodes(__node_id__ [, _relationships_ ] [, _traverse_ ] [, _flags_ ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| node_id       | JSON Object | Yes      | N/A           | N/A      |
| relationships | Boolean     | No       | False         | <ul><li>True</li><li>False</li></ul> |
| traverse      | String      | No       | N/A           | "NodeKind:Relationship:NodeKind:Node" |
| flags         | String      | No       | N/A           | <ul><li>"include_destroyed"</li><li>"exclude_current"</li></ul> |

Example:

```python
>>> node = data.get_data_nodes("a1b2c3d4e5f6")
>>> print(node.json()['state']['os_type'])
Windows Desktop
```

## get_data_nodes_graph()

Graph data represents a set of nodes and relationships that are associated to the given node.

Syntax:

```
.get_data_nodes_graph(__node_id__ [, _focus_ ] [, _apply_rules_ ] [, _complete_ ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| node_id       | JSON Object | Yes      | N/A           | N/A      |
| focus         | String      | No       | N/A           | <ul><li>"software-connected"</li><li>"software"</li><li>"infrastructure"</li></ul> |
| apply_rules   | Boolean     | No       | False         | <ul><li>True</li><li>False</li></ul> |
| complete      | Boolean     | No       | False         | <ul><li>True</li><li>False</li></ul> |

## get_data_kinds()

Finds all nodes of a specified node kind.

Syntax:

```
.get_data_kinds(__kind__ [, _offset_ ] [, _results_id_ ] [, _format_ ] [, _limit_ ] [, _delete_ ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| kind          | String      | Yes      | N/A           | Any node kind |
| offset        | Integer     | No       | N/A           | N/A      |
| results_id    | String      | No       | N/A           | N/A      |
| format        | String      | No       | N/A           | "object" |
| limit         | Integer     | No       | 100           | N/A      |
| delete        | Boolean     | No       | False         | <ul><li>True</li><li>False</li></ul> |

Example: Gets result #50 from list of nodes

```python
>>> sis = data.get_data_kinds("SoftwareInstance")
>>> print(sis.json()[0]['results'][50])
['0x7761771a5876f667606e53426', 'Apache Webserver', 'Apache Webserver 2.4 on batman3', '2.4', 'batman3']
```

## get_data_kinds_values()

Retrieve values for an attribute of a node kind.

Syntax:

```
.get_data_kinds_values(__kind__, __attribute__ [, _offset_ ] [, _results_id_ ] [, _format_ ] [, _limit_ ] [, _delete_ ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| kind          | String      | Yes      | N/A           | Any node kind |
| attribute     | String      | Yes      | N/A           | N/A |
| offset        | Integer     | No       | N/A           | N/A |
| results_id    | String      | No       | N/A           | N/A |
| format        | String      | No       | N/A           | "object" |
| limit         | Integer     | No       | 100           | N/A |
| delete        | Boolean     | No       | False         | <ul><li>True</li><li>False</li></ul> |

## get_data_partitions

Graph data represents a set of nodes and relationships that are associated to the given node.

Syntax:

```
.get_data_partitions()
```

Example:

```python
>>> partitions = data.get_data_partitions()
>>> from pprint import pprint
>>> pprint(partitions.json())
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

## searchQuery()

[Deprecated] See [search](#search) for usage.

Syntax: `.searchQuery(__json__ [, _offset_ ] [, _results_id_ ] [, _format_ ] [, _limit_ ] [, _delete_ ])`

## nodeLookup()

[Deprecated] See [get_data_nodes](#get_data_nodes) for usage.

Syntax: `.nodeLookup(__node_id__ [, _relationships_ ] [, _traverse_ ] [, _flags_ ])`

## lookupNodeKind()

[Deprecated] See [get_data_kinds](#get_data_kinds) for usage.

Syntax: `.lookupNodeKind(__kind__ [, _offset_ ] [, _results_id_ ] [, _format_ ] [, _limit_ ] [, _delete_ ])`

## graphNode()

[Deprecated] See [get_data_nodes_graph](#get_data_nodes_graph) for usage.

Syntax: `.graphNode(__node_id__ [, _focus_ ] [, _apply_rules_ ]))`

## partitions()

[Deprecated] See [get_data_nodes_graph](#get_data_nodes_graph) for usage.

Syntax: `.partitions()`

## post_data_partitions()

Create a Partition.

Syntax:

```
.post_data_partitions(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |

## post_data_import()

Imports data. Returns the import UUID.

Syntax:

```

.post_data_import(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |

## post_data_import_graph()

Import graph data. Returns the import UUID.

Syntax:

```
.post_data_import_graph(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |

## post_data_write()

Perform arbitrary write operations.

Syntax:

```
.post_data_write(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |

## get_data_external_consumer()

Retrieve external consumer information. With no arguments all consumers are returned.

Syntax:

```
.get_data_external_consumer([ _consumer_name_ ] [, _path_ ])
```

| Parameters    | Type   | Required | Default Value | Options |
| ------------- | ------ | :------: | ------------- | ------- |
| consumer_name | String | No       | N/A           | N/A     |
| path          | String | No       | N/A           | N/A     |

## post_data_external_consumer()

Create or interact with an external consumer resource.

Syntax:

```
.post_data_external_consumer(__json__ [, _consumer_name_ ] [, _path_ ])
```

| Parameters    | Type        | Required | Default Value | Options |
| ------------- | ----------- | :------: | ------------- | ------- |
| json          | JSON Object | Yes      | N/A           | N/A     |
| consumer_name | String      | No       | N/A           | N/A     |
| path          | String      | No       | N/A           | N/A     |

## patch_data_external_consumer()

Update an external consumer resource.

Syntax:

```
.patch_data_external_consumer(__consumer_name__, __json__ [, _path_ ])
```

| Parameters    | Type        | Required | Default Value | Options |
| ------------- | ----------- | :------: | ------------- | ------- |
| consumer_name | String      | Yes      | N/A           | N/A     |
| json          | JSON Object | Yes      | N/A           | N/A     |
| path          | String      | No       | N/A           | N/A     |

## delete_data_external_consumer()

Delete an external consumer resource.

Syntax:

```
.delete_data_external_consumer(__consumer_name__ [, _path_ ])
```

| Parameters    | Type   | Required | Default Value | Options |
| ------------- | ------ | :------: | ------------- | ------- |
| consumer_name | String | Yes      | N/A           | N/A     |
| path          | String | No       | N/A           | N/A     |

## best_candidate()

[Deprecated] See [post_data_candidate](#post_data_candidate) for usage.

Syntax: `.post_data_candidate(__JSON__)`

## top_candidates()

[Deprecated] See [post_data_candidates](#post_data_candidates) for usage.

Syntax: `.post_data_candidates(__json__)`

## twImport()

[Deprecated] See [post_data_import](#post_data_import) for usage.

Syntax: `.twImport(__json__)`

## twWrite()

[Deprecated] See [post_data_write](#post_data_write) for usage.

Syntax: `.twWrite(__json__)`