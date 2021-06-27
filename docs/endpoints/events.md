---
sort: 7
---

# Events

- Initiate an Event object for the instance of Discovery you intend to query.

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> events = tw.events()
```

## status()

- Returns a unique ID if the event has been recorded, otherwise an empty string is returned e.g. if the event source has been disabled.

Syntax: `status(*json*)`

| Parameters | Type | Use
| - | - | -
| **json** | JSON | Required |

```python
>>> events.status({"source":"Event1","type":"EventType1"}
})
```