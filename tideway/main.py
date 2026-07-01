#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from . import discoRequests as dr
from . import endpoints
import tideway

class Appliance:
    '''An appliance instance.'''

    def __init__(self, target, token, limit = 100, delete = False, api_version = "1.16", ssl_verify = False):
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

    def get(self, endpoint, response="application/json"):
        '''Request any endpoint.'''
        req = dr.discoRequest(self, endpoint, response=response)
        self.reset_params()
        return req

    def post(self, endpoint, body=None, response="application/json", files=None, data=None, content_type=None):
        '''Post any endpoint.'''
        req = dr.discoPost(
            self,
            endpoint,
            body,
            response=response,
            files=files,
            data=data,
            content_type=content_type,
        )
        self.reset_params()
        return req

    def delete(self, endpoint, response="application/json"):
        '''Delete any endpoint.'''
        req = dr.discoDelete(self, endpoint, response=response)
        self.reset_params()
        return req

    def patch(self, endpoint, body, response="application/json"):
        '''Patch any endpoint.'''
        req = dr.discoPatch(self, endpoint, body, response=response)
        self.reset_params()
        return req

    def put(self, endpoint, body, response="application/json"):
        '''Update any endpoint.'''
        req = dr.discoPut(self, endpoint, body, response=response)
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
        tx = tideway.taxonomy(self.target, self.token, api_version=self.api_version, ssl_verify=self.verify)
        return tx

    def topology(self):
        t = tideway.topology(self.target, self.token, api_version=self.api_version, ssl_verify=self.verify)
        return t

    def vault(self):
        v = tideway.vault(self.target, self.token, api_version=self.api_version, ssl_verify=self.verify)
        return v

    ### API Admin ###

    @property
    def api_about(self):
        '''Altnernate API call for /about.'''
        url = self.api + "/about"
        req = requests.get(url, verify=self.verify)
        return req

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
    def api_help(self):
        '''Help on endpoints.'''
        endpoints.docs()
        #print("")

    def help(self, endpoint=None):
        '''Help on endpoints.'''
        if endpoint:
            endpoints.docs(endpoint)
        else:
            endpoints.docs()
        #print("\n")

### Discovery Admin ###

    @property
    def get_admin_baseline(self):
        '''Alternate API call for baseline.'''
        return self.get("/admin/baseline")

    @property
    def get_admin_about(self):
        '''Alternate API call for /admin/about.'''
        return self.get("/admin/about")

    @property
    def get_admin_licensing(self):
        '''Alternate API call for licensing report.'''
        return self.get("/admin/licensing", response="text/plain")

    @property
    def get_admin_licensing_csv(self):
        '''Alternate API call for licensing report CSV.'''
        return self.get("/admin/licensing/csv", response="application/zip")
    
    @property
    def get_admin_licensing_raw(self):
        '''Alternate API call for licensing report raw.'''
        return self.get("/admin/licensing/raw", response="application/zip")
