#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

# Disable Insecure SSL warning
requests.packages.urllib3.disable_warnings()

def url_and_headers(target,apiendpoint,token,response):
    url = "https://" + str(target) + "/api/v1.1" + apiendpoint
    headers = {"Accept": response, "Authorization":"bearer " + str(token) }
    return url, headers

def discoRequest(ip, token, apirequest, params=None,response="application/json"):
    url, heads = url_and_headers(ip,apirequest,token,response)
    if params:
        req = requests.get(url, headers=heads, params=params, verify=False)
    else:
        req = requests.get(url, headers=heads, verify=False)
    return req

def discoPost(ip, token, apipost, jsoncode, params=None, response="application/json"):
    url, heads = url_and_headers(ip,apipost,token,response)
    if params:
        req = requests.post(url, json=jsoncode, headers=heads, params=params, verify=False)
    else:
        req = requests.post(url, json=jsoncode, headers=heads, verify=False)
    return req

def filePost(ip, token, apipost, file, params=None, response="text/html"):
    files = {"file":open(file,'rb')}
    url, heads = url_and_headers(ip,apipost,token,response)
    if params:
        req = requests.post(url, files=files, headers=heads, params=params, verify=False)
    else:
        req = requests.post(url, files=files, headers=heads, verify=False)
    return req

def discoPatch(ip, token, apipatch, jsoncode, params=None, response="application/json"):
    url, heads = url_and_headers(ip,apipatch,token,response)
    if params:
        req = requests.patch(url, json=jsoncode, headers=heads, params=params, verify=False)
    else:
        req = requests.patch(url, json=jsoncode, headers=heads, verify=False)
    return req

def discoPut(ip, token, apiput, jsoncode, params=None, response="application/json"):
    url, heads = url_and_headers(ip,apiput,token,response)
    if params:
        req = requests.put(url, json=jsoncode, headers=heads, params=params, verify=False)
    else:
        req = requests.put(url, json=jsoncode, headers=heads, verify=False)
    return req

def discoDelete(ip, token, del_node, params=None, response="application/json"):
    url, heads = url_and_headers(ip,del_node,token,response)
    if params:
        req = requests.delete(url, headers=heads, params=params, verify=False)
    else:
        req = requests.delete(url, headers=heads, verify=False)
    return req

class discovery():
    '''Control scanning and view results.'''

    def __init__(self, ip, token, limit = None, delete = False):
        self.ip = ip
        self.token = token
        self.params = {}
        if limit:
            self.params['limit'] = limit
        if delete:
            self.params['delete'] = delete

    def getDiscoveryStatus(self):
        '''Get the current status of the discovery process.'''
        response = discoRequest(self.ip, self.token, "/discovery")
        return response

    def setDiscoveryStatus(self, jsoncode):
        '''Either start or stop the discovery process. Note this call can return before the desired state has been reached.'''
        response = discoPatch(self.ip, self.token, "/discovery", jsoncode)
        return response

    def getDiscoveryCloudMetaData(self):
        '''Get metadata for the cloud providers currently supported by BMC Discovery.'''
        response = discoRequest(self.ip, self.token, "/discovery/cloud_metadata")
        return response

    def getDiscoveryRuns(self):
        '''Get details of all currently processing discovery runs.'''
        response = discoRequest(self.ip, self.token, "/discovery/runs")
        return response

    def getDiscoveryRun(self, runid):
        '''Get details of specific currently processing discovery run.'''
        response = discoRequest(self.ip, self.token, "/discovery/runs/{}".format(runid))
        return response

    def discoveryRun(self, jsoncode):
        '''Create a new snapshot discovery run.'''
        response = discoPost(self.ip, self.token, "/discovery/runs", jsoncode)
        return response

    def updateDiscoveryRun(self, runid, jsoncode):
        '''Update the state of a specific discovery run.'''
        response = discoPatch(self.ip, self.token, "/discovery/runs/{}".format(runid), jsoncode)
        return response

    def getDiscoveryRunResults(self, runid):
        '''Get a summary of the results from scanning all endpoints in the run, partitioned by result type.'''
        response = discoRequest(self.ip, self.token, "/discovery/runs/{}/results".format(runid))
        return response

    def getDiscoveryRunResult(self, runid, result="Success", offset=None, results_id=None, format=None):
        '''Get a summary of the results from scanning all endpoints in the run that had a specific type of result.'''
        if offset:
            self.params['offset'] = offset
        if results_id:
            self.params['results_id'] = results_id
        if format:
            self.params['format'] = format
        response = discoRequest(self.ip, self.token, "/discovery/runs/{}/results/{}".format(runid,result), params=self.params)
        return response

    def getDiscoveryRunInferred(self, runid):
        '''Get a summary of all inferred devices from a discovery run, partitioned by device type.'''
        response = discoRequest(self.ip, self.token, "/discovery/runs/{}/inferred".format(runid))
        return response

    def getDiscoveryRunInferredKind(self, runid, inferred_kind, offset=None, results_id=None, format=None):
        '''Get a summary of the devices inferred by a discovery run which have a specific inferred kind.'''
        if offset:
            self.params['offset'] = offset
        if results_id:
            self.params['results_id'] = results_id
        if format:
            self.params['format'] = format
        response = discoRequest(self.ip, self.token, "/discovery/runs/{}/inferred/{}".format(runid,inferred_kind), params=self.params)
        return response

class data():
    '''Retrieve data from the model.'''
    def __init__(self, ip, token, limit = None, delete = False):
        self.ip = ip
        self.token = token
        self.params = {}
        if limit:
            self.params['limit'] = limit
        if delete:
            self.params['delete'] = delete

    def search(self, query, offset=None, results_id=None, format=None):
        '''Run a search query, receiving paginated results.'''
        self.params['query'] = query
        if offset:
            self.params['offset'] = offset
        if results_id:
            self.params['results_id'] = results_id
        if format:
            self.params['format'] = format
        response = discoRequest(self.ip, self.token, "/data/search", params=self.params)
        return response

    def searchQuery(self, body, offset=None, results_id=None, format=None):
        '''An alternative to GET /data/search, for search queries which are too long for urls.'''
        if format:
            self.params['format'] = format
        response = discoPost(self.ip, self.token, "/data/search", body, params=self.params)
        return response

    def nodeLookup(self, node_id, relationships=False, traverse=None, flags=None):
        '''Get the state of a node with specified id.'''
        if traverse:
            self.params['traverse'] = traverse
            if flags:
                self.params['flags'] = flags
        if offset:
            self.params['offset'] = offset
        if results_id:
            self.params['results_id'] = results_id
        if format:
            self.params['format'] = format
        if relationships:
            response = discoRequest(self.ip, self.token, "/data/nodes/{}?relationships=true".format(node_id), params=self.params)
        else:
            response = discoRequest(self.ip, self.token, "/data/nodes/{}".format(node_id), params=self.params)
        return response

    def graphNode(self, node_id, focus="sofware-connected", apply_rules=True):
        '''Graph data represents a set of nodes and relationships that are associated to the given node.'''
        if focus:
            self.params['focus'] = focus
        if apply_rules:
            self.params['apply_rules'] = apply_rules
        response = discoRequest(self.ip, self.token, "/data/nodes/{}/graph".format(node_id), params=self.params)
        return response

    def lookupNodeKind(self, kind, offset=None, results_id=None, format=None):
        '''Finds all nodes of a specified node kind.'''
        if offset:
            self.params['offset'] = offset
        if results_id:
            self.params['results_id'] = results_id
        if format:
            self.params['format'] = format
        response = discoRequest(self.ip, self.token, "/data/kinds/{}".format(kind), params=self.params)
        return response

class vault():
    '''Manage the credential vault.'''
    def __init__(self, ip, token):
        self.ip = ip
        self.token = token

    def getVault(self):
        '''Get details of the state of the vault.'''
        response = discoRequest(self.ip, self.token, "/vault")
        return response

    def updateVault(self, jsoncode):
        '''Change the state of the vault.'''
        response = discoPatch(self.ip, self.token, "/vault", jsoncode)
        return response

class credentials():
    '''Manage credentials.'''

    def __init__(self, ip, token):
        self.ip = ip
        self.token = token
        self.params = {}

    def listCredentialTypes(self, group=None, category=None):
        '''Get a list of all credential types and filter by group and/or category.'''
        if group:
            self.params['group'] = group
        if category:
            self.params['category'] = category
        response = discoRequest(self.ip, self.token, "/vault/credential_types", params=self.params)
        return response

    def credentialType(self, cred_type_name):
        '''Get the properties of a specific credential type.'''
        response = discoRequest(self.ip, self.token, "/vault/credential_types/{}".format(cred_type_name))
        return response

    def listCredentials(self, cred_id=None):
        '''Get a list of all credentials.'''
        if cred_id:
            response = discoRequest(self.ip, self.token, "/vault/credentials/{}".format(cred_id))
        else:
            response = discoRequest(self.ip, self.token, "/vault/credentials")
        return response

    def newCredential(self, body):
        '''Create a new credential.'''
        response = discoPost(self.ip, self.token, "/vault/credentials", body)
        return response

    def deleteCredential(self, cred_id):
        '''Delete a credential.'''
        response = discoDelete(self.ip, self.token, "/vault/credentials/{}".format(cred_id))
        return response

    def updateCredential(self, cred_id, body):
        '''Updates partial resources of a credential. Missing properties are left unchanged.'''
        response = discoPatch(self.ip, self.token, "/vault/credentials/{}".format(cred_id), body)
        return response

    def replaceCredential(self, cred_id, body):
        '''Replaces a single credential. All required credential properties must be present. Optional properties that are missing will be reset to their defaults.'''
        response = discoPut(self.ip, self.token, "/vault/credentials/{}".format(cred_id), body)
        return response

class knowledge():
    '''Upload new TKUs and pattern modules.'''

    def __init__(self, ip, token):
        self.ip = ip
        self.token = token
        self.params = {}

    def getKnowledgeManagement(self):
        '''Get the current state of the appliance's knowledge, including TKU versions.'''
        response = discoRequest(self.ip, self.token, "/knowledge")
        return response

    def getUploadStatus(self):
        '''Get the current state of a knowledge upload.'''
        response = discoRequest(self.ip, self.token, "/knowledge/status")
        return response

    def uploadKnowledge(self, filename, file, activate=True, allow_restart=False):
        '''Upload a TKU or pattern module to the appliance.'''
        if activate:
            self.params['activate'] = activate
        if allow_restart:
            self.params['allow_restart'] = allow_restart
        response = filePost(self.ip, self.token, "/knowledge/{}".format(filename), file, params=self.params)
        return response

class events():
    '''Push events.'''

    def __init__(self, ip, token):
        self.ip = ip
        self.token = token

    def status(self, body):
        '''Returns a unique ID if the event has been recorded, otherwise an empty string is returned e.g. if the event source has been disabled.'''
        response = discoPost(self.ip, self.token, "/events", body)
        return response

class admin():
    '''Manage the BMC Discovery appliance.'''

    def __init__(self, ip, token):
        self.ip = ip
        self.token = token

    def baseline(self):
        '''Get a summary of the appliance status, and details of which baseline checks have passed or failed.'''
        response = discoRequest(self.ip, self.token, "/admin/baseline")
        return response

    def about(self):
        '''Get information about the appliance, like its version and versions of the installed packages.'''
        response = discoRequest(self.ip, self.token, "/admin/about")
        return response

    def licensing(self,content_type="text/plain"):
        '''Get the latest signed licensing report.'''
        if content_type == "csv":
            response = discoRequest(self.ip, self.token, "/admin/licensing/csv",response="application/zip")
        elif content_type == "raw":
            response = discoRequest(self.ip, self.token, "/admin/licensing/raw",response="application/zip")
        else:
            response = discoRequest(self.ip, self.token, "/admin/licensing",response=content_type)
        return response
