---
sort: 8
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

## getNodes()

Get topology data from one or more starting nodes.

Syntax:

```
.getNodes(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |

## getNodeKinds()

Get nodes of the specified kinds which are related to a given set of nodes.

Syntax:

```
.getNodeKinds(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |

## visualizationState()

Get the current state of the visualization for the authenticated user.

Syntax:

```
.visualizationState()
```

## updateVizState()

Update one or more attributes of the current state of the visualization for the authenticated user.

Syntax:
```
.updateVizState(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |

## replaceVizState()

Update any or all of the attributes of the current state of the visualization for the authenticated user.

Syntax:
```
replaceVizState(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |
