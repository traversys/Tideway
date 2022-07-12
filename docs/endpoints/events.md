---
sort: 6
---

# Events

Initiate an Event object for the instance of Discovery you intend to query.

Syntax:

```
tideway.events(__target__, __token__ [, _api_version_ ] [, _ssl_verify_ ])
```

Initiation:

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> events = tw.events()
```

## post_events()

Returns a unique ID if the event has been recorded, otherwise an empty string is returned e.g. if the event source has been disabled.

Syntax: 

```
.post_events(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |

## status()

[Deprecated] See [post_events](#post_events) for usage.

Syntax: `.status(__json__)`