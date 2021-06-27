---
sort: 9
---

# Admin

- Initiate an Admin object for the instance of Discovery you intend to query.

```python
>>> import tideway
>>> ta = tideway.admin('appliance-hostname','auth-token')
```

## baseline()

- Get a summary of the appliance status, and details of which baseline checks have passed or failed.

```python
>>> ta.baseline().json()
{
    "results": {
        "FAILED": [
            {
                "enabled": true,
                "message": "MAJOR: This appliance has insufficent resources",
                "name": "Appliance Specification",
                "severity": "MAJOR"
            },
            {
                "details": [
                    {
                        "messages": [
                            "2 credentials have been added",
...
```

## about()

- Get information about the appliance, like its version and versions of the installed packages.

```python
>>> ta.about()
{
    "versions": {
        "devices": "5.0.2020.09.3",
        "os_updates": "7.20.08.25",
        "product": "12.1",
        "product_content": "2.0.2020.09.3"
    }
}
```

## licensing()

- Get the latest signed licensing report.
- CSV option returns raw license data in CSV format as a zip file for offline analysis.
- RAW option return an encrypted raw license object for import to another appliance.

Syntax: `licensing([ content_type=*optional* (default="text/plain") ])`

| Parameters | Type | Use | Options
| - | - | - | -
| content_type=**string** | String | | "text/plain"<br>"csv"<br>"raw" |

```python
>>> ta.licensing()
-----BEGIN LICENSE REPORT-----
License report
==============

Report start time: 2021-01-18 23:00:00.409987+00:00
Report end time  : 2021-01-21 23:00:00.410085+00:00
...
```