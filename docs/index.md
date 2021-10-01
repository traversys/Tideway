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
        "1.2"
    ],
    "component": "REST API",
    "product": "BMC Discovery",
    "version": "12.2"
}
```

Tideway follows BMC Discovery's well-structured and documented REST API which can be viewed from `https://<appliance>/swagger-ui/`.

Tideway removes the extra layer of manually constructing a URL and parameters for python requests allowing you to query API supported features of Discovery seamlessly and faster than if you were to navigate via the GUI.

## Installation

- Tideway can be installed via PyPI:

```console
$ python -m pip install tideway
```

- Tideway supports BMC Discovery 11.3+, API v1.2 using Python 3.

## Contents

{% include list.liquid all=true %}

## Releases

| Version | Summary                                                | Known Issues                                                   | Fixed                          |
| :-----: | ------------------------------------------------------ | -------------------------------------------------------------- | ------------------------------ |
| 0.1.0   | Initial release, compatible with API v1.1              |                                                                |                                |
| 0.1.1   | Updated to API v1.2<br>Added `help()`, `search_bulk()` | search call retains last parameters for `offset`, `results_id` |                                |
| 0.1.2   | Bug Fixes | Bulk search with larger limit than dataset will fail on missing `next_offset` | Fixed issue with `offset` and `results_id` values<br>Fixed issue with bulk search parameter lower limit. |
| 0.1.3   | Bug Fixes                                              |                                                                | Added check for `next_offset`. |
| 0.1.4   | Search bulk update | Discovery 12.3 (21.3) enforces strict case for "Bearer" header - api calls will not current work.  | Now includes headers for non-formatted search. |
| 0.1.5   | Updated to support Discovery 12.3 (API version 1.3)    |                                                                | Fixed issue with Bearer capitalisation.<br>Search Bulk will now return the full response on failure |
