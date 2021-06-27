---
sort: 8
---

# Topology

- Initiate a Topology object for the instance of Discovery you intend to query.

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> topo = tw.topology()
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
>>> topo.graphNode("a1b2c3d4e5f6")
```

## getNodes()

- Get topology data from one or more starting nodes.

Syntax: `getNodes(*json*)`

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required |

## getNodeKinds()

- Get nodes of the specified kinds which are related to a given set of nodes.

Syntax: `getNodeKinds(*json*)`

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required |

## visualizationState()

- Get the current state of the visualization for the authenticated user.

## updateVizState()

- Update one or more attributes of the current state of the visualization for the authenticated user.

Syntax: `updateVizState(*json*)`

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required |

## replaceVizState()

- Update any or all of the attributes of the current state of the visualization for the authenticated user.

Syntax: `replaceVizState(*json*)`

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required |
