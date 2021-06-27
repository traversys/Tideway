---
sort: 3
---

# Data

- Initiate a Data object for the instance of Discovery you intend to query.

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> data = tw.data()
```

## search()

- Run a search query, receiving paginated results.

Syntax: `search(*query* [, offset=*optional* ] [, results_id=*optional* ] [, format=*optional* ] [, limit=*optional*] [, delete=*optional*])`

| Parameters | Type | Use | Options | Default
| - | - | - | - | -
| **query** | String or JSON | Required | "search string"<br>{"query":"search string"} | |
| offset=**integer** | Integer | | | |
| results_id=**string** | String | | | |
| format=**string** | String | | "object" |
| limit=**integer** | Integer | | | 100 |
| delete=**boolean** | Boolean | | | False |

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

## search_bulk()

- Run a search bulk search query, will loop paginated results and return all results as a JSON list object. The function makes use of results_id and offset automatically so these are not required as arguments.

```note
This function may take a long time to run as it will be run multiple API calls until the entire query is fulfilled.
```

Syntax: `search_bulk(*query* [, format=*optional* ] [, limit=*optional*] [, delete=*optional*])`

| Parameters | Type | Use | Options | Default
| - | - | - | - | -
| **query** | String or JSON | Required | "search string"<br>{"query":"search string"} | |
| format=**string** | String | | "object" |
| limit=**integer** | Integer | | | 100 |
| delete=**boolean** | Boolean | | | False |

```python
>>> data.search_bulk("search Host show name", limit=500)
```

## searchQuery()

- An alternative to GET /data/search, for search queries which are too long for urls.

```note
This method is deprecated. You can use search() for both JSON arguments and search strings.
```

Syntax: `searchQuery(*json* [, offset=*optional* ] [, results_id=*optional* ] [, format=*optional* ] [, limit=*optional*] [, delete=*optional*])`

| Parameters | Type | Use | Options | Default
| - | - | - | - | -
| **json** | JSON | Required | {"query":"search string"}
| offset=**intger** | Integer | | |
| results_id=**string** | String | | |
| format=**string** | String | | "object"
| limit=**integer** | Integer | | | 100 |
| delete=**boolean** | Boolean | | | False |

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

- Get the state of a node with specified id.

Syntax: `nodeLookup(*node_id* [, relationships=*optional* (default=*False*) ] [, traverse=*optional* ] [, flags=*optional* ])`

| Parameters | Type | Use | Options
| - | - | - | -
| **node_id** | JSON | Required | |
| relationships=**boolean** | String | | True<br>False
| traverse=**string** | String | | "NodeKind:Relationship:NodeKind:Node"
| flags=**string** | String | | "include_destroyed"<br>"exclude_current" |

```python
>>> data.nodeLookup("a1b2c3d4e5f6")
```

## lookupNodeKind()

- Finds all nodes of a specified node kind.

Syntax: `lookupNodeKind(*kind* [, offset=*optional* ] [, results_id=*optional* ] [, format=*optional* ] [, limit=*optional*] [, delete=*optional*])`

| Parameters | Type | Use | Options | Default
| - | - | - | - | -
| **kind** | String | Required | |
| offset=**intger** | Integer | | |
| results_id=**string** | String | | |
| format=**string** | String | | "object"
| limit=**integer** | Integer | | | 100 |
| delete=**boolean** | Boolean | | | False |

```python
>>> data.lookupNodeKind("Host")
```

## graphNode()

- Graph data represents a set of nodes and relationships that are associated to the given node.

Syntax: `graphNode(*node_id* [, focus=*optional* (default=*"sofware-connected"*)] [, apply_rules=*optional* (default=*True*) ])`

| Parameters | Type | Use | Options
| - | - | - | -
| **node_id** | JSON | Required | |
| focus=**string** | String | | "software-connected"<br>"software"<br>"infrastructure"
| apply_rules=**boolean** | Boolean | | True<br>False

```python
>>> data.graphNode("a1b2c3d4e5f6")
```

## partitions()

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

## candidate()

- The node object of the best candidate based on the provided parameters.

Syntax: `candidate(*json*)`

```python
>>> data.candidate({})
```

## candidates()

- Enter parameters to identify a device, the response is a list of candidate nodes ordered by descending score.

Syntax: `candidates(*json*)`

```python
>>> data.candidates({})
```

## twImport()

- Imports data. Returns the import UUID.

Syntax: `twImport(*json*)`

### twWrite()

- Perform arbitrary write operations.

Syntax: `twWrite(*json*)`