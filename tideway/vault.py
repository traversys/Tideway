# -*- coding: utf-8 -*-

import tideway
import warnings

dr = tideway.discoRequests
appliance = tideway.main.Appliance

class Vault(appliance):
    '''Manage the credential vault.'''

    def get_vault(self):
        '''Get details of the state of the vault.'''
        return dr.discoRequest(self, "/vault")

    def getVault(self):
        '''Get details of the state of the vault.'''
        warnings.warn(
            "getVault() is deprecated; use get_vault() instead.",
            DeprecationWarning,
        )
        return self.get_vault()
    get_vault_property = property(get_vault)

    def patch_vault(self, body):
        '''Alternate API call for PATCH /vault'''
        response = dr.discoPatch(self, "/vault", body)
        return response

    def updateVault(self, body):
        '''Change the state of the vault.'''
        warnings.warn(
            "updateVault() is deprecated; use patch_vault() instead.",
            DeprecationWarning,
        )
        return self.patch_vault(body)
