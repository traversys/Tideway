#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

# Disable Insecure SSL warning
requests.packages.urllib3.disable_warnings()

def discoRequest(ip, token, apirequest, params=None):
    url = "https://" + str(ip) + "/api/v1.1" + apirequest
    heads = {"Accept": "application/json", "Authorization":"bearer " + str(token) }
    if params:
        req = requests.get(url, headers=heads, params=params, verify=False)
    else:
        req = requests.get(url, headers=heads, verify=False)
    return req

def discoPost(ip, token, apipost, jsoncode, params=None):
    url = "https://" + str(ip) + "/api/v1.1" + apipost
    heads = {"Accept": "application/json", "Authorization":"bearer " + str(token) }
    if params:
        req = requests.post(url, json=jsoncode, headers=heads, params=params, verify=False)
    else:
        req = requests.post(url, json=jsoncode, headers=heads, verify=False)
    return req

def discoPatch(ip, token, apipatch, jsoncode, params=None):
    url = "https://" + str(ip) + "/api/v1.1" + apipatch
    heads = {"Accept": "application/json", "Authorization":"bearer " + str(token) }
    if params:
        req = requests.patch(url, json=jsoncode, headers=heads, params=params, verify=False)
    else:
        req = requests.patch(url, json=jsoncode, headers=heads, verify=False)
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
    def __init__(self, ip, token, limit = None, delete = False):
        self.ip = ip
        self.token = token
        self.params = {}
        if limit:
            self.params['limit'] = limit
        if delete:
            self.params['delete'] = delete

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

class knowledge():
    '''Upload new TKUs and pattern modules.'''

class events():
    '''Push events.'''

class admin():
    '''Manage the BMC Discovery appliance.'''
