import requests

# Disable Insecure SSL warning
requests.packages.urllib3.disable_warnings()

def url_and_headers(target,token,api_endpoint,response):
    url = target + api_endpoint
    headers = {"Accept": response, "Authorization":"Bearer " + str(token) }
    return url, headers

def discoRequest(appliance, api_endpoint, response="application/json"):
    url, heads = url_and_headers(appliance.url, appliance.token, api_endpoint, response)
    req = requests.get(url, headers=heads, params=appliance.params.copy(), verify=appliance.verify)
    appliance.reset_params()
    return req

def discoPost(appliance, api_endpoint, jsoncode, response="application/json"):
    url, heads = url_and_headers(appliance.url, appliance.token, api_endpoint, response)
    req = requests.post(url, json=jsoncode, headers=heads, params=appliance.params.copy(), verify=appliance.verify)
    appliance.reset_params()
    return req

def filePost(appliance, api_endpoint, file, response="text/html"):
    url, heads = url_and_headers(appliance.url, appliance.token, api_endpoint, response)
    with open(file, 'rb') as f:
        files = {"file": f}
        req = requests.post(url, files=files, headers=heads, params=appliance.params.copy(), verify=appliance.verify)
    appliance.reset_params()
    return req

def keytabPost(appliance, api_endpoint, file, username, response="application/json", content_type="multipart/form-data"):
    url, heads = url_and_headers(appliance.url, appliance.token, api_endpoint, response)
    heads['Content-type'] = content_type
    with open(file, 'rb') as f:
        form_data = {"keytab": f, "username": username}
        req = requests.post(url, files=form_data, headers=heads, params=appliance.params.copy(), verify=appliance.verify)
    appliance.reset_params()
    return req

def discoPatch(appliance, api_endpoint, jsoncode, response="application/json"):
    url, heads = url_and_headers(appliance.url, appliance.token, api_endpoint, response)
    req = requests.patch(url, json=jsoncode, headers=heads, params=appliance.params.copy(), verify=appliance.verify)
    appliance.reset_params()
    return req

def discoPut(appliance, api_endpoint, jsoncode, response="application/json"):
    url, heads = url_and_headers(appliance.url, appliance.token, api_endpoint, response)
    req = requests.put(url, json=jsoncode, headers=heads, params=appliance.params.copy(), verify=appliance.verify)
    appliance.reset_params()
    return req

def discoDelete(appliance, api_endpoint, response="application/json"):
    url, heads = url_and_headers(appliance.url, appliance.token, api_endpoint, response)
    req = requests.delete(url, headers=heads, params=appliance.params.copy(), verify=appliance.verify)
    appliance.reset_params()
    return req
