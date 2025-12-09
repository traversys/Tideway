import requests

# Disable Insecure SSL warning
requests.packages.urllib3.disable_warnings()

def url_and_headers(target,token,api_endpoint,response):
    url = target + api_endpoint
    headers = {"Accept": response, "Authorization":"Bearer " + str(token) }
    return url, headers

def discoRequest(appliance, api_endpoint, response="application/json"):
    """Issue a GET request."""
    url, heads = url_and_headers(appliance.url, appliance.token, api_endpoint, response)
    req = requests.get(url, headers=heads, params=appliance.params.copy(), verify=appliance.verify)
    appliance.reset_params()
    return req

def discoPost(appliance, api_endpoint, jsoncode=None, response="application/json", files=None, data=None, content_type=None):
    """Issue a POST request with optional JSON, form data, or files."""
    url, heads = url_and_headers(appliance.url, appliance.token, api_endpoint, response)
    if content_type:
        heads['Content-type'] = content_type
    req = requests.post(
        url,
        json=jsoncode if files is None else None,
        files=files,
        data=data,
        headers=heads,
        params=appliance.params.copy(),
        verify=appliance.verify,
    )
    appliance.reset_params()
    return req

def filePost(appliance, api_endpoint, file, response="text/html"):
    """Backward compatible helper for file uploads."""
    with open(file, 'rb') as f:
        files = {"file": f}
        req = discoPost(appliance, api_endpoint, files=files, response=response)
    return req

def keytabPost(appliance, api_endpoint, file, username, response="application/json", content_type="multipart/form-data"):
    """Backward compatible helper for Kerberos uploads."""
    with open(file, 'rb') as f:
        form_data = {"keytab": f, "username": username}
        req = discoPost(appliance, api_endpoint, files=form_data, response=response, content_type=content_type)
    return req

def discoPatch(appliance, api_endpoint, jsoncode, response="application/json"):
    """Issue a PATCH request."""
    url, heads = url_and_headers(appliance.url, appliance.token, api_endpoint, response)
    req = requests.patch(url, json=jsoncode, headers=heads, params=appliance.params.copy(), verify=appliance.verify)
    appliance.reset_params()
    return req

def discoPut(appliance, api_endpoint, jsoncode, response="application/json"):
    """Issue a PUT request."""
    url, heads = url_and_headers(appliance.url, appliance.token, api_endpoint, response)
    req = requests.put(url, json=jsoncode, headers=heads, params=appliance.params.copy(), verify=appliance.verify)
    appliance.reset_params()
    return req

def discoDelete(appliance, api_endpoint, response="application/json"):
    """Issue a DELETE request."""
    url, heads = url_and_headers(appliance.url, appliance.token, api_endpoint, response)
    req = requests.delete(url, headers=heads, params=appliance.params.copy(), verify=appliance.verify)
    appliance.reset_params()
    return req
