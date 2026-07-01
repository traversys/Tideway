# Tideway

Tideway is a simplified Python library for the BMC Discovery REST API. It uses the Python Requests module [https://github.com/psf/requests](https://github.com/psf/requests) and returns standard `requests.Response` objects for direct API calls.


```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> tw.api_about.url
'https://appliance-hostname/api/about'
>>> tw.api_about.status_code
200
>>> tw.api_about.text
{
    "api_versions": [
        "1.0","1.1","1.2","1.3","1.4","1.5","1.6","1.7","1.8","1.9","1.10","1.11","1.12","1.13","1.14","1.15","1.16"
    ],
    "component": "REST API",
    "version":"DaaS",
    "product": "BMC Helix Discovery",
    "version": "25.2.00"
}
```

Tideway follows BMC Discovery's well-structured and documented REST API which can be viewed from `https://<appliance>/swagger-ui/`.

Tideway removes the extra layer of manually constructing a URL and parameters for python requests allowing you to query API supported features of Discovery seamlessly and faster than if you were to navigate via the GUI.

Example notebook: [`notebooks/admin_api.ipynb`](https://github.com/traversys/Tideway/blob/main/notebooks/admin_api.ipynb) (download via `curl -O https://raw.githubusercontent.com/traversys/Tideway/main/notebooks/admin_api.ipynb`)

## Installation

Tideway can be installed via PyPI:

```console
$ python -m pip install tideway
```

## Quick Start

Create an appliance or outpost client, then use either direct REST wrappers or endpoint-specific clients.

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname', 'auth-token')
>>> tw.get('/admin/about').json()
{
    ...
}
>>> data = tw.data()
>>> hosts = data.search('search Host show name', limit=100)
>>> len(hosts)
100
```

Endpoint-specific clients are available from the appliance object:

```python
>>> tw.admin()
>>> tw.credentials()
>>> tw.data()
>>> tw.discovery()
>>> tw.events()
>>> tw.kerberos()
>>> tw.knowledge()
>>> tw.models()
>>> tw.taxonomy()
>>> tw.topology()
>>> tw.vault()
```

For schema discovery and endpoint help:

```python
>>> tw.api_schema()
>>> tw.api_paths('/data/search')
>>> tw.help('/data/search')
```

## Contents

- [Quickstart Guide](quickstart/readme.md)
  - [Object Initiation](quickstart/initiation.md)
  - [Responses](quickstart/responses.md)
- [API Endpoints](endpoints/readme.md)
  - [Admin](endpoints/admin.md)
  - [Appliance or Outpost](endpoints/appliance.md)
  - [Credentials](endpoints/credentials.md)
  - [Data](endpoints/data.md)
  - [Discovery](endpoints/discovery.md)
  - [Events](endpoints/events.md)
  - [Kerberos](endpoints/kerberos.md)
  - [Knowledge](endpoints/knowledge.md)
  - [Models](endpoints/models.md)
  - [Taxonomy](endpoints/taxonomy.md)
  - [Topology](endpoints/topology.md)
  - [Vault](endpoints/vault.md)
  - [Security](endpoints/security.md)

## Releases

| Version | Summary                   | Known Issues                                       | Fixed                            |
| :-----: | ------------------------- | -------------------------------------------------- | -------------------------------- | 
| 0.1.1   | - Updated to API v1.2<br>- Added `help()`, `search_bulk()` | search call retains last parameters for `offset`, `results_id` | |
| 0.1.2   | Bug Fixes | Bulk search with larger limit than dataset will fail on missing `next_offset` | - Fixed issue with `offset` and `results_id` values<br>- Fixed issue with bulk search parameter lower limit. |
| 0.1.3   | Bug Fixes                 |                                                    | Added check for `next_offset`.   |
| 0.1.4   | Search bulk update        | Discovery 12.3 (21.3) enforces strict case for "Bearer" header - api calls will not current work. | Now includes headers for non-formatted search. |
| 0.1.5   | Updated to support Discovery 12.3 (API version 1.3) | - Missing 'complete' parameter option on graphNode() function. | - Fixed issue with Bearer capitalisation.<br>- Search Bulk will now return the full response on failure |
| 0.2.0   | Updated to include Kerberos, Models and Taxonomy endpoints.<br><br>Added new high level generic endpoint function calls<br><br>Refactored function names/decorators to match API endpoints as close as possible.<br><br>Supports Discovery 22.2 (12.5) (API version 1.5) and Outpost API version 1.0 | Project missing tkinter module: https://github.com/traversys/Tideway/issues/15 | Added 'complete' parameter to `get_data_nodes_graph()` (replaces `graphNode()`) |
| 0.2.1   | Added `complete` flag for graph calls, bug fixes to pagination and default focus.<br><br>Can retrieve condition templates without an ID.<br><br>Kerberos realm detection fixed and parameters are reset after each request.<br><br>Removed unused Tkinter library.<br><br>Updated to support API version 1.14 | May not work with all new endpoints. | | Issue: https://github.com/traversys/Tideway/issues/15 |
| 0.3.0   | Refreshed package metadata and documentation for the current API surface.<br><br>Added schema helpers, updated endpoint docs, and fixed the appliance `taxonomy()` shortcut. | | Docs and runtime help table updated; PyPI build artifacts refreshed. |
