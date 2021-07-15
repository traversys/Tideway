---
sort: 3
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

## search()

Run a search query, receiving paginated results.

Syntax:

```
.search(__query__ [, _offset_ ] [, _results_id_ ] [, _format_ ] [, _limit_ ] [, _delete_ ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| query | <ul><li>String</li><li>JSON Object</li></ul> | Yes | N/A | <ul><li>"search string"</li><li>{"query":"search string"}</li></ul> |
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

## searchQuery()

An alternative to GET /data/search, for search queries which are too long for urls.

```note
This method is deprecated. You can use search() for both JSON arguments and search strings.
```

Syntax:

```
.search(__json__ [, _offset_ ] [, _results_id_ ] [, _format_ ] [, _limit_ ] [, _delete_ ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | {"query":"search string"} |
| offset        | Integer     | No       | N/A           | N/A      |
| results_id    | String      | No       | N/A           | N/A      |
| format        | String      | No       | N/A           | <ul><li>"object"</li><li>"tree"</li></ul> |
| limit         | Integer     | No       | 100           | N/A      |
| delete        | Boolean     | No       | False         | <ul><li>True</li><li>False</li></ul> |

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

## nodeLookup()

Get the state of a node with specified id.

Syntax:

```
.nodeLookup(__node_id__ [, _relationships_ ] [, _traverse_ ] [, _flags_ ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| node_id       | JSON Object | Yes      | N/A           | N/A      |
| relationships | Boolean     | No       | False         | <ul><li>True</li><li>False</li></ul> |
| traverse      | String      | No       | N/A           | "NodeKind:Relationship:NodeKind:Node" |
| flags         | String      | No       | N/A           | <ul><li>"include_destroyed"</li><li>"exclude_current"</li></ul> |

Example:

```python
>>> node = data.nodeLookup("a1b2c3d4e5f6")
>>> print(node.json()['state']['os_type'])
Windows Desktop
```

## lookupNodeKind()

Finds all nodes of a specified node kind.

Syntax:

```
.lookupNodeKind(__kind__ [, _offset_ ] [, _results_id_ ] [, _format_ ] [, _limit_ ] [, _delete_ ])
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
>>> sis = data.lookupNodeKind("SoftwareInstance")
>>> print(sis.json()[0]['results'][50])
['0x7761771a5876f667606e53426', 'Apache Webserver', 'Apache Webserver 2.4 on batman3', '2.4', 'batman3']
```

## graphNode()

Graph data represents a set of nodes and relationships that are associated to the given node.

Syntax:

```
.graphNode(__node_id__ [, _focus_ ] [, _apply_rules_ ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| node_id       | JSON Object | Yes      | N/A           | N/A      |
| focus         | String      | No       | N/A           | <ul><li>"software-connected"</li><li>"software"</li><li>"infrastructure"</li></ul> |
| apply_rules   | Boolean     | No       | False         | <ul><li>True</li><li>False</li></ul> |

## partitions()

Graph data represents a set of nodes and relationships that are associated to the given node.

Syntax:

```
.partitions()
```

Example:

```python
>>> partitions = data.partions()
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

## candidate()

The node object of the best candidate based on the provided parameters.

Syntax:

```
.candidate(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |

## candidates()

Enter parameters to identify a device, the response is a list of candidate nodes ordered by descending score.

Syntax:

```
.candidates(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |

## twImport()

Imports data. Returns the import UUID.

Syntax:

```
.twImport(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |

## twWrite()

Perform arbitrary write operations.

Syntax:

```
.twWrite(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |