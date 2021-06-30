---
sort: 7
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

## status()

Returns a unique ID if the event has been recorded, otherwise an empty string is returned e.g. if the event source has been disabled.

Syntax: 

```
.status(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |
