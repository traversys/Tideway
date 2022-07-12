#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import BASELINE
import requests
from . import discoRequests as dr
from . import endpoints
import tideway

class Appliance:
    '''An appliance instance.'''

    def __init__(self, target, token, limit = 100, delete = False, api_version = "1.5", ssl_verify = False):
        self.target = target
        self.token = token
        self.params = {}
        self.params['limit'] = limit
        self.params['delete'] = delete
        self.api_version = api_version
        self.target_url = "https://" + str(target)
        self.api = self.target_url + "/api"
        self.url = self.api + "/v" + self.api_version
        self.verify = ssl_verify

    def get(self,endpoint):
        '''Request any endpoint.'''
        req = dr.discoRequest(self,endpoint)
        return req

    def post(self,endpoint,body):
        '''Post any endpoint.'''
        req = dr.discoPost(self, endpoint, body)
        return req

    def delete(self,endpoint):
        '''Delete any endpoint.'''
        req = dr.discoDelete(self, endpoint)
        return req

    def patch(self,endpoint,body):
        '''Patch any endpoint.'''
        req = dr.discoPatch(self, endpoint, body)
        return req

    def put(self,endpoint,body):
        '''Update any endpoint.'''
        req = dr.discoPut(self, endpoint, body)
        return req

    def credentials(self):
        c = tideway.credentials(self.target, self.token, api_version=self.api_version, ssl_verify=self.verify)
        return c

    def data(self):
        d = tideway.data(self.target, self.token, api_version=self.api_version, ssl_verify=self.verify)
        return d

    def discovery(self):
        di = tideway.discovery(self.target, self.token, api_version=self.api_version, ssl_verify=self.verify)
        return di

    def events(self):
        e = tideway.events(self.target, self.token, api_version=self.api_version, ssl_verify=self.verify)
        return e

    def kerberos(self):
        ks = tideway.kerberos(self.target, self.token, api_version=self.api_version, ssl_verify=self.verify)
        return ks

    def knowledge(self):
        k = tideway.knowledge(self.target, self.token, api_version=self.api_version, ssl_verify=self.verify)
        return k

    def models(self):
        m = tideway.models(self.target, self.token, api_version=self.api_version, ssl_verify=self.verify)
        return m

    def taxonomy(self):
        tx = tideway.topology(self.target, self.token, api_version=self.api_version, ssl_verify=self.verify)
        return tx

    def topology(self):
        t = tideway.topology(self.target, self.token, api_version=self.api_version, ssl_verify=self.verify)
        return t

    def vault(self):
        v = tideway.vault(self.target, self.token, api_version=self.api_version, ssl_verify=self.verify)
        return v

    ### Admin ###

    @property
    def api_about(self):
        '''Altnernate API call for /about.'''
        url = self.api + "/about"
        req = requests.get(url, verify=self.verify)
        return req

    def about(self):
        '''Return about data.'''
        url = self.api + "/about"
        req = requests.get(url, verify=self.verify)
        return req

    @property
    def api_swagger(self):
        '''Alternate API call for swagger.'''
        url = self.url + "/swagger.json"
        req = requests.get(url, verify=self.verify)
        return req

    def swagger(self):
        '''Get swagger file.'''
        url = self.url + "/swagger.json"
        req = requests.get(url, verify=self.verify)
        return req

    @property
    def get_admin_baseline(self):
        '''Alternate API call for baseline.'''
        response = dr.discoRequest(self, "/admin/baseline")
        return response

    def baseline(self):
        '''Get a summary of the appliance status, and details of which baseline checks have passed or failed.'''
        response = dr.discoRequest(self, "/admin/baseline")
        return response

    @property
    def get_admin_about(self):
        '''Alternate API call for /admin/about.'''
        response = dr.discoRequest(self, "/admin/about")
        return response

    def admin(self):
        '''Get information about the appliance, like its version and versions of the installed packages.'''
        response = dr.discoRequest(self, "/admin/about")
        return response

    @property
    def get_admin_licensing(self):
        '''Alternate API call for licensing report.'''
        response = dr.discoRequest(self, "/admin/licensing",response="text/plain")
        return response

    @property
    def get_admin_licensing_csv(self):
        '''Alternate API call for licensing report CSV.'''
        response = dr.discoRequest(self, "/admin/licensing/csv",response="application/zip")
        return response
    
    @property
    def get_admin_licensing_raw(self):
        '''Alternate API call for licensing report raw.'''
        response = dr.discoRequest(self, "/admin/licensing/raw",response="application/zip")
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

    @property
    def api_help(self):
        '''Help on endpoints.'''
        endpoints.docs()
        #print("")

    def help(*args):
        '''Help on endpoints.'''
        if len(args) > 1:
            endpoints.docs(args[1])
        else:
            endpoints.docs()
        #print("\n")