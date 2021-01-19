#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

# Disable Insecure SSL warning
requests.packages.urllib3.disable_warnings()

def discoRequest(ip, token, query):
    try:
        url = "https://" + str(ip) + "/api/v1.1" + query
        heads = {"Accept": "application/json", "Authorization":"bearer " + str(token) }
        req = requests.get(url, headers=heads, verify=False)
    except:
        req = "Something wrong with request input!"
    return req

def discoPost(ip, token, query, jsoncode):
    try:
        url = "https://" + str(ip) + "/api/v1.1" + query
        heads = {"Accept": "application/json", "Authorization":"bearer " + str(token) }
        req = requests.post(url, json=jsoncode, headers=heads, verify=False)
    except:
        req = "Something wrong with request input!"
    return req

def discoPatch(ip, token, patch, jsoncode):
    try:
        url = "https://" + str(ip) + "/api/v1.1" + patch
        heads = {"Accept": "application/json", "Authorization":"bearer " + str(token) }
        req = requests.patch(url, json=jsoncode, headers=heads, verify=False)
    except:
        req = "Something wrong with request input!"
    return req

class discovery():
    '''Control scanning and view results.'''

    def getDiscoveryStatus(self, ip, token):
        '''Get the current status of the discovery process.'''
        response = discoRequest(ip, token, "/discovery")
        return response

    def setDiscoveryStatus(self, ip, token, jsoncode):
        '''Either start or stop the discovery process. Note this call can return before the desired state has been reached.'''
        response = discoPatch(ip, token, "/discovery", jsoncode)
        return response

    def getDiscoveryCloudMetaData(self, ip, token):
        '''Get metadata for the cloud providers currently supported by BMC Discovery.'''
        response = discoRequest(ip, token, "/discovery/cloud_metadata")
        return response

    def getDiscoveryRuns(self, ip, token):
        '''Get details of all currently processing discovery runs.'''
        response = discoRequest(ip, token, "/discovery/runs")
        return response

    def discoveryRun(self, ip, token, jsoncode):
        '''Either start or stop the discovery process. Note this call can return before the desired state has been reached.'''
        response = discoPost(ip, token, "/discovery/runs", jsoncode)
        return response

class data():
    '''Retrieve data from the model.'''

class vault():
    '''Manage the credential vault.'''

class credentials():
    '''Manage credentials.'''

class knowledge():
    '''Upload new TKUs and pattern modules.'''

class events():
    '''Push events.'''

class admin():
    '''Manage the BMC Discovery appliance.'''
