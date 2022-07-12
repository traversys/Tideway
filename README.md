# Tideway

Simplified Python library for BMC Discovery API Interface that makes use of the Python Requests module [https://github.com/psf/requests](https://github.com/psf/requests) and uses the same response handler.


```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> tw.about().url
'https://appliance-hostname/api/about'
>>> tw.about().status_code
200
>>> tw.about().text
{
    "api_versions": [
        "1.0",
        "1.1",
        "1.2",
        "1.3",
        "1.4",
        "1.5"
    ],
    "component": "REST API",
    "product": "BMC Discovery",
    "version": "12.5"
}
```

Tideway follows BMC Discovery's well-structured and documented REST API which can be viewed from `https://<appliance>/swagger-ui/`.

Tideway removes the extra layer of manually constructing a URL and parameters for python requests allowing you to query API supported features of Discovery seamlessly and faster than if you were to navigate via the GUI.

## Documentation

Documentation can be found at [https://traversys.github.io/Tideway/](https://traversys.github.io/Tideway/).

## Releases

| Version | Summary                   | Known Issues                                       | Fixed                            |
| :-----: | ------------------------- | -------------------------------------------------- | -------------------------------- | 
| 0.1.1   | - Updated to API v1.2<br>- Added `help()`, `search_bulk()` | search call retains last parameters for `offset`, `results_id` | |
| 0.1.2   | Bug Fixes | Bulk search with larger limit than dataset will fail on missing `next_offset` | - Fixed issue with `offset` and `results_id` values<br>- Fixed issue with bulk search parameter lower limit. |
| 0.1.3   | Bug Fixes                 |                                                    | Added check for `next_offset`.   |
| 0.1.4   | Search bulk update        | Discovery 12.3 (21.3) enforces strict case for "Bearer" header - api calls will not current work. | Now includes headers for non-formatted search. |
| 0.1.5   | Updated to support Discovery 12.3 (API version 1.3) | - Missing 'complete' parameter option on graphNode() function. | - Fixed issue with Bearer capitalisation.<br>- Search Bulk will now return the full response on failure |
| 0.2.0   | Updated to include Kerberos, Models and Taxonomy endpoints.<br><br>Added new high level generic endpoint function calls<br><br>Refactored function names/decorators to match API endpoints as close as possible.<br><br>Supports Discovery 22.2 (12.5) (API version 1.5) and Outpost API version 1.0 | Not all new unctions have been tested. | Added 'complete' parameter to `get_data_nodes_graph()` (replaces `graphNode()`) |
