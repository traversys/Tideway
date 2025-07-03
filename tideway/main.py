#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from . import discoRequests as dr
from . import endpoints
import tideway
import warnings

class Appliance:
    '''An appliance instance.'''

    def __init__(self, target, token, limit = 100, delete = False, api_version = "1.14", ssl_verify = False):
        self.target = target
        self.token = token
        self.default_limit = limit
        self.default_delete = delete
        self.params = {}
        self.reset_params()
        self.api_version = api_version
        self.target_url = "https://" + str(target)
        self.api = self.target_url + "/api"
        self.url = self.api + "/v" + self.api_version
        self.verify = ssl_verify

    def reset_params(self):
        '''Reset request parameters back to default.'''
        self.params.clear()
        self.params['limit'] = self.default_limit
        self.params['delete'] = self.default_delete

    def get(self,endpoint):
        '''Request any endpoint.'''
        req = dr.discoRequest(self,endpoint)
        self.reset_params()
        return req

    def post(self,endpoint,body):
        '''Post any endpoint.'''
        req = dr.discoPost(self, endpoint, body)
        self.reset_params()
        return req

    def delete(self,endpoint):
        '''Delete any endpoint.'''
        req = dr.discoDelete(self, endpoint)
        self.reset_params()
        return req

    def patch(self,endpoint,body):
        '''Patch any endpoint.'''
        req = dr.discoPatch(self, endpoint, body)
        self.reset_params()
        return req

    def put(self,endpoint,body):
        '''Update any endpoint.'''
        req = dr.discoPut(self, endpoint, body)
        self.reset_params()
        return req

    def admin(self):
        a = tideway.admin(self.target, self.token, api_version=self.api_version, ssl_verify=self.verify)
        return a
    
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
        warnings.warn(
            "about() is deprecated; use api_about instead.",
            DeprecationWarning,
        )
        return self.api_about

    def _get_api_schema(self):
        '''Helper to fetch API schema, trying /swagger.json first, then /openapi.json.'''
        for path in ["/swagger.json", "/openapi.json"]:
            url = self.url + path
            req = requests.get(url, verify=self.verify)
            if req.status_code != 404:
                return req
        return req  # return the last response (likely 404 if both failed)

    @property
    def api_swagger(self):
        '''Alternate API call for swagger.'''
        return self._get_api_schema()

    def swagger(self):
        '''Fetch API schema, trying /swagger.json first, then /openapi.json.'''
        warnings.warn(
            "swagger() is deprecated; use api_swagger instead.",
            DeprecationWarning,
        )
        return self.api_swagger

    def _load_schema(self):
        '''Return cached API schema as dict, fetching it if necessary.'''
        if getattr(self, '_api_schema', None) is None:
            response = self.api_swagger
            self._api_schema = response.json() if response.ok else {}
        return self._api_schema

    def api_schema(self):
        '''Return the parsed API schema.'''
        return self._load_schema()

    def api_paths(self, path=None):
        '''Return all available API paths or details for a specific path.'''
        paths = self._load_schema().get('paths', {})
        if path:
            return paths.get(path)
        return paths

    @property
    def get_admin_baseline(self):
        '''Alternate API call for baseline.'''
        response = dr.discoRequest(self, "/admin/baseline")
        return response

    def baseline(self):
        '''Get a summary of the appliance status, and details of which baseline checks have passed or failed.'''
        warnings.warn(
            "baseline() is deprecated; use get_admin_baseline instead.",
            DeprecationWarning,
        )
        return self.get_admin_baseline

    @property
    def get_admin_about(self):
        '''Alternate API call for /admin/about.'''
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