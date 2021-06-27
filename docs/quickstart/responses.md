---
sort: 2
---


# Responses

## Input

```python
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> response = tw.about()
```

## .headers
```python
>>> tw.about().headers
{'Date': 'Sun, 06 Jun 2021 18:43:31 GMT', 'Server': 'waitress', 'X-Content-Type-Options': 'nosniff', 'Content-Length': '160', 'Content-Type': 'application/json', 'Content-security-policy': "default-src https: 'self'; style-src https: 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline' 'unsafe-eval' blob:; img-src 'self' data:; base-uri 'none'; object-src 'none'; connect-src https: 'self'; frame-ancestors 'self';", 'Keep-Alive': 'timeout=15, max=100', 'Connection': 'Keep-Alive'}
```
## .encoding
```python
>>> tw.about().encoding
None
```
## .elapsed
```python
>>> tw.about().elapsed
0:00:00.028861
```
## .content
```python
>>> tw.about().content
b'{\n    "api_versions": [\n        "1.0",\n        "1.1",\n        "1.2"\n    ],\n    "component": "REST API",\n    "product": "BMC Discovery",\n    "version": "12.2"\n}\n'
```
## .cookies
```python
>>> tw.about().cookies
<RequestsCookieJar[]>
```
## .history
```python
>>> tw.about().history
[]
```
## .is_permanent_redirect
```python
>>> tw.about().is_permanent_redirect
False
```
## .is_redirect
```python
>>> tw.about().is_redirect
False
```
## .iter_content()
```python
>>> tw.about().iter_content()
<generator object iter_slices at 0x7fc1252a8820>
```
## .json()
```python
>>> tw.about().json()
{'api_versions': ['1.0', '1.1', '1.2'], 'component': 'REST API', 'product': 'BMC Discovery', 'version': '12.2'}
```
## .url
```python
>>> tw.about().url
https://appliance-hostname/api/about
```
## .text
```python
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
## .status_code
```python
>>> tw.about().status_code
200
```
## .request
```python
>>> tw.about().request
<PreparedRequest [GET]>
```
## .reason
```python
>>> tw.about().reason
OK
```
## .raise_for_status()
```python
>>> tw.about().raise_for_status()
None
```
## .ok
```python
>>> tw.about().ok
True
```
## links
```python
>>> tw.about().links
{}
```