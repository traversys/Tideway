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

## Contents

- [Tideway](#tideway)
  - [Contents](#contents)
  - [Installation](#installation)

## Installation

- Tideway can be installed via PyPI:

```console
$ python -m pip install tideway
```

- Tideway supports BMC Discovery 11.3+, API v1.2 using Python 3.
