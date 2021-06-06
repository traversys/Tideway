#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from . import discoRequests as dr
from . import endpoints
import tideway

class Appliance:
    '''An appliance instance.'''

    def __init__(self, target, token, limit = 100, delete = False, api_version = "1.2", ssl_verify = False):
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

    def knowing(self):
        k = tideway.knowledge(self.target, self.token)
        return k

    ### Admin ###

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

    def baseline(self):
        '''Get a summary of the appliance status, and details of which baseline checks have passed or failed.'''
        response = dr.discoRequest(self, "/admin/baseline")
        return response

    def admin(self):
        '''Get information about the appliance, like its version and versions of the installed packages.'''
        response = dr.discoRequest(self, "/admin/about")
        return response

    def licensing(self,content_type="text/plain"):
        '''Get the latest signed licensing report.'''
        if content_type == "csv":
            response = dr.discoRequest(self, "/admin/licensing/csv",response="application/zip")
        elif content_type == "raw":
            response = dr.discoRequest(self, "/admin/licensing/raw",response="application/zip")
        else:
            response = dr.discoRequest(self, "/admin/licensing",response=content_type)
        return response

    def help(*args):
        '''Help on endpoints.'''
        if len(args) > 1:
            endpoints.docs(args[1])
        else:
            endpoints.docs()
        print("")
