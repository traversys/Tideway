---
sort: 11
---

# Topology

Initiate a Topology object for the instance of Discovery you intend to query.

Syntax:

```
tideway.topology(__target__, __token__ [, _api_version_ ] [, _ssl_verify_ ])
```

Initiation:

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> topo = tw.topology()
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

## post_topology_nodes()

Get topology data from one or more starting nodes.

Syntax:

```
.post_topology_nodes(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |

## post_topology_nodes_kinds()

Get nodes of the specified kinds which are related to a given set of nodes.

Syntax:

```
.post_topology_nodes_kinds(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |

## graphNode()

[Deprecated] See [get_data_nodes_graph](#get_data_nodes_graph) for usage.

Syntax: `.graphNode(__node_id__ [, _focus_ ] [, _apply_rules_ ])`

## getNodes()

[Deprecated] See [post_topology_nodes](#post_topology_nodes) for usage.

Syntax: `.getNodes(__json__)`

## getNodeKinds()

[Deprecated] See [post_topology_nodes_kinds](#post_topology_nodes_kinds) for usage.

Syntax: `.getNodeKinds(__json__)`

## get_topology_viz_state

Get the current state of the visualization for the authenticated user.

Syntax:

```
.get_topology_viz_state
```

## patch_topology_viz_state()

Update one or more attributes of the current state of the visualization for the authenticated user.

Syntax:
```
.patch_topology_viz_state(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |


## put_topology_viz_state()

Update any or all of the attributes of the current state of the visualization for the authenticated user.

Syntax:
```
put_topology_viz_state(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |

## visualizationState()

[Deprecated] See [get_topology_viz_state](#get_topology_viz_state) for usage.

Syntax: `.visualizationState()`

## updateVizState()

[Deprecated] See [patch_topology_viz_state](#patch_topology_viz_state) for usage.

Syntax: `.updateVizState(__json__)`

## replaceVizState()

[Deprecated] See [put_topology_viz_state](#put_topology_viz_state) for usage.

Syntax: `.replaceVizState(__json__)`