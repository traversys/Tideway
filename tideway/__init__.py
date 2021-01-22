#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

# Disable Insecure SSL warning
requests.packages.urllib3.disable_warnings()

def url_and_headers(target,token,api_endpoint,response):
    url = target + api_endpoint
    headers = {"Accept": response, "Authorization":"bearer " + str(token) }
    return url, headers

def discoRequest(appliance, api_endpoint, response="application/json"):
    url, heads = url_and_headers(appliance.url,appliance.token,api_endpoint,response)
    req = requests.get(url, headers=heads, params=appliance.params, verify=appliance.verify)
    return req

def discoPost(appliance, api_endpoint, jsoncode, response="application/json"):
    url, heads = url_and_headers(appliance.url,appliance.token,api_endpoint,response)
    req = requests.post(url, json=jsoncode, headers=heads, params=appliance.params, verify=appliance.verify)
    return req

def filePost(appliance, api_endpoint, file, response="text/html"):
    files = {"file":open(file,'rb')}
    url, heads = url_and_headers(appliance.url,appliance.token,api_endpoint,response)
    req = requests.post(url, files=files, headers=heads, params=appliance.params, verify=appliance.verify)
    return req

def discoPatch(appliance, api_endpoint, jsoncode, response="application/json"):
    url, heads = url_and_headers(appliance.url,appliance.token,api_endpoint,response)
    req = requests.patch(url, json=jsoncode, headers=heads, params=appliance.params, verify=appliance.verify)
    return req

def discoPut(appliance, api_endpoint, jsoncode, response="application/json"):
    url, heads = url_and_headers(appliance.url,appliance.token,api_endpoint,response)
    req = requests.put(url, json=jsoncode, headers=heads, params=appliance.params, verify=appliance.verify)
    return req

def discoDelete(appliance, api_endpoint, response="application/json"):
    url, heads = url_and_headers(appliance.url,appliance.token,api_endpoint,response)
    req = requests.delete(url, headers=heads, params=appliance.params, verify=appliance.verify)
    return req

class appliance:
    '''An appliance instance.'''

    def __init__(self, target, token, limit = 100, delete = False, api_version = "1.1", ssl_verify = False):
        self.target = target
        self.token = token
        self.params = {}
        self.params['limit'] = limit
        if delete:
            self.params['delete'] = delete
        self.api_version = api_version
        self.api = "https://" + str(target) + "/api"
        self.url = self.api + "/v" + self.api_version
        self.verify = ssl_verify

    def about(self):
        '''Return about info for API.'''
        url = self.api + "/about"
        req = requests.get(url, verify=self.verify)
        return req

    def swagger(self):
        '''Get swagger file.'''
        url = self.url + "/swagger.json"
        req = requests.get(url, verify=self.verify)
        return req

class discovery(appliance):
    '''Control scanning and view results.'''

    def getDiscoveryStatus(self):
        '''Get the current status of the discovery process.'''
        response = discoRequest(self, "/discovery")
        return response

    def setDiscoveryStatus(self, body):
        '''Either start or stop the discovery process. Note this call can return before the desired state has been reached.'''
        response = discoPatch(self, "/discovery", body)
        return response

    def getDiscoveryCloudMetaData(self):
        '''Get metadata for the cloud providers currently supported by BMC Discovery.'''
        response = discoRequest(self, "/discovery/cloud_metadata")
        return response

    def getDiscoveryRuns(self):
        '''Get details of all currently processing discovery runs.'''
        response = discoRequest(self, "/discovery/runs")
        return response

    def getDiscoveryRun(self, runid):
        '''Get details of specific currently processing discovery run.'''
        response = discoRequest(self, "/discovery/runs/{}".format(runid))
        return response

    def discoveryRun(self, body):
        '''Create a new snapshot discovery run.'''
        response = discoPost(self, "/discovery/runs", body)
        return response

    def updateDiscoveryRun(self, runid, body):
        '''Update the state of a specific discovery run.'''
        response = discoPatch(self, "/discovery/runs/{}".format(runid), body)
        return response

    def getDiscoveryRunResults(self, runid):
        '''Get a summary of the results from scanning all endpoints in the run, partitioned by result type.'''
        response = discoRequest(self, "/discovery/runs/{}/results".format(runid))
        return response

    def getDiscoveryRunResult(self, runid, result="Success", offset=None, results_id=None, format=None):
        '''Get a summary of the results from scanning all endpoints in the run that had a specific type of result.'''
        if offset:
            self.params['offset'] = offset
        if results_id:
            self.params['results_id'] = results_id
        if format:
            self.params['format'] = format
        response = discoRequest(self, "/discovery/runs/{}/results/{}".format(runid,result))
        return response

    def getDiscoveryRunInferred(self, runid):
        '''Get a summary of all inferred devices from a discovery run, partitioned by device type.'''
        response = discoRequest(self, "/discovery/runs/{}/inferred".format(runid))
        return response

    def getDiscoveryRunInferredKind(self, runid, inferred_kind, offset=None, results_id=None, format=None):
        '''Get a summary of the devices inferred by a discovery run which have a specific inferred kind.'''
        if offset:
            self.params['offset'] = offset
        if results_id:
            self.params['results_id'] = results_id
        if format:
            self.params['format'] = format
        response = discoRequest(self, "/discovery/runs/{}/inferred/{}".format(runid,inferred_kind))
        return response

class data(appliance):
    '''Retrieve data from the model.'''

    def search(self, query, offset=None, results_id=None, format=None):
        '''Run a search query, receiving paginated results.'''
        self.params['query'] = query
        if offset:
            self.params['offset'] = offset
        if results_id:
            self.params['results_id'] = results_id
        if format:
            self.params['format'] = format
        response = discoRequest(self, "/data/search")
        return response

    def searchQuery(self, body, offset=None, results_id=None, format=None):
        '''An alternative to GET /data/search, for search queries which are too long for urls.'''
        if format:
            self.params['format'] = format
        response = discoPost(self, "/data/search", body)
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
            response = discoRequest(self, "/data/nodes/{}?relationships=true".format(node_id))
        else:
            response = discoRequest(self, "/data/nodes/{}".format(node_id))
        return response

    def graphNode(self, node_id, focus="sofware-connected", apply_rules=True):
        '''Graph data represents a set of nodes and relationships that are associated to the given node.'''
        if focus:
            self.params['focus'] = focus
        if apply_rules:
            self.params['apply_rules'] = apply_rules
        response = discoRequest(self, "/data/nodes/{}/graph".format(node_id))
        return response

    def lookupNodeKind(self, kind, offset=None, results_id=None, format=None):
        '''Finds all nodes of a specified node kind.'''
        if offset:
            self.params['offset'] = offset
        if results_id:
            self.params['results_id'] = results_id
        if format:
            self.params['format'] = format
        response = discoRequest(self, "/data/kinds/{}".format(kind))
        return response

class vault(appliance):
    '''Manage the credential vault.'''

    def getVault(self):
        '''Get details of the state of the vault.'''
        response = discoRequest(self, "/vault")
        return response

    def updateVault(self, body):
        '''Change the state of the vault.'''
        response = discoPatch(self, "/vault", body)
        return response

class credentials(appliance):
    '''Manage credentials.'''

    def listCredentialTypes(self, group=None, category=None):
        '''Get a list of all credential types and filter by group and/or category.'''
        if group:
            self.params['group'] = group
        if category:
            self.params['category'] = category
        response = discoRequest(self, "/vault/credential_types")
        return response

    def credentialType(self, cred_type_name):
        '''Get the properties of a specific credential type.'''
        response = discoRequest(self, "/vault/credential_types/{}".format(cred_type_name))
        return response

    def listCredentials(self, cred_id=None):
        '''Get a list of all credentials.'''
        if cred_id:
            response = discoRequest(self, "/vault/credentials/{}".format(cred_id))
        else:
            response = discoRequest(self, "/vault/credentials")
        return response

    def newCredential(self, body):
        '''Create a new credential.'''
        response = discoPost(self, "/vault/credentials", body)
        return response

    def deleteCredential(self, cred_id):
        '''Delete a credential.'''
        response = discoDelete(self, "/vault/credentials/{}".format(cred_id))
        return response

    def updateCredential(self, cred_id, body):
        '''Updates partial resources of a credential. Missing properties are left unchanged.'''
        response = discoPatch(self, "/vault/credentials/{}".format(cred_id), body)
        return response

    def replaceCredential(self, cred_id, body):
        '''Replaces a single credential. All required credential properties must be present. Optional properties that are missing will be reset to their defaults.'''
        response = discoPut(self, "/vault/credentials/{}".format(cred_id), body)
        return response

class knowledge(appliance):
    '''Upload new TKUs and pattern modules.'''

    def getKnowledgeManagement(self):
        '''Get the current state of the appliance's knowledge, including TKU versions.'''
        response = discoRequest(self, "/knowledge")
        return response

    def getUploadStatus(self):
        '''Get the current state of a knowledge upload.'''
        response = discoRequest(self, "/knowledge/status")
        return response

    def uploadKnowledge(self, filename, file, activate=True, allow_restart=False):
        '''Upload a TKU or pattern module to the appliance.'''
        if activate:
            self.params['activate'] = activate
        if allow_restart:
            self.params['allow_restart'] = allow_restart
        response = filePost(self, "/knowledge/{}".format(filename), file)
        return response

class events(appliance):
    '''Push events.'''

    def status(self, body):
        '''Returns a unique ID if the event has been recorded, otherwise an empty string is returned e.g. if the event source has been disabled.'''
        response = discoPost(self, "/events", body)
        return response

class admin(appliance):
    '''Manage the BMC Discovery appliance.'''

    def baseline(self):
        '''Get a summary of the appliance status, and details of which baseline checks have passed or failed.'''
        response = discoRequest(self, "/admin/baseline")
        return response

    def about(self):
        '''Get information about the appliance, like its version and versions of the installed packages.'''
        response = discoRequest(self, "/admin/about")
        return response

    def licensing(self,content_type="text/plain"):
        '''Get the latest signed licensing report.'''
        if content_type == "csv":
            response = discoRequest(self, "/admin/licensing/csv",response="application/zip")
        elif content_type == "raw":
            response = discoRequest(self, "/admin/licensing/raw",response="application/zip")
        else:
            response = discoRequest(self, "/admin/licensing",response=content_type)
        return response
