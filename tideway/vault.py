# -*- coding: utf-8 -*-

import requests
import tideway

dr = tideway.discoRequests
appliance = tideway.main.Appliance

class Vault(appliance):
    '''Manage the credential vault.'''

    def getVault(self):
        '''Get details of the state of the vault.'''
        response = dr.discoRequest(self, "/vault")
        return response

    def updateVault(self, body):
        '''Change the state of the vault.'''
        response = dr.discoPatch(self, "/vault", body)
        return response
