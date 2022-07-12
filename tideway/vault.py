# -*- coding: utf-8 -*-

import tideway

dr = tideway.discoRequests
appliance = tideway.main.Appliance

class Vault(appliance):
    '''Manage the credential vault.'''

    def getVault(self):
        '''Get details of the state of the vault.'''
        response = dr.discoRequest(self, "/vault")
        return response
    get_vault = property(getVault)

    def patch_vault(self, body):
        '''Alternate API call for PATCH /vault'''
        response = dr.discoPatch(self, "/vault", body)
        return response

    def updateVault(self, body):
        '''Change the state of the vault.'''
        response = dr.discoPatch(self, "/vault", body)
        return response
