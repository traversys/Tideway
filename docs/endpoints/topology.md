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

## graphNode(*node_id* [, focus=*optional* (default=*"sofware-connected"*)] [, apply_rules=*optional* (default=*True*) ])

| Parameters | Type | Use | Options
| - | - | - | -
| **node_id** | JSON | Required | |
| focus=**string** | String | | "software-connected"<br>"software"<br>"infrastructure"
| apply_rules=**boolean** | Boolean | | True<br>False

- Graph data represents a set of nodes and relationships that are associated to the given node.

```python
>>> topo.graphNode("a1b2c3d4e5f6")
```

## getNodes(*json*)

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required |

- Get topology data from one or more starting nodes.

## getNodeKinds(*json*)

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required |

- Get nodes of the specified kinds which are related to a given set of nodes.

## visualizationState()

- Get the current state of the visualization for the authenticated user.

## updateVizState(*json*)

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required |

- Update one or more attributes of the current state of the visualization for the authenticated user.

## replaceVizState(*json*)

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required |

- Update any or all of the attributes of the current state of the visualization for the authenticated user.
