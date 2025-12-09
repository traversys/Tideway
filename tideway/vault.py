# -*- coding: utf-8 -*-

import tideway

appliance = tideway.main.Appliance

class Vault(appliance):
    '''Manage the credential vault.'''

    def get_vault(self):
        '''Get details of the state of the vault.'''
        return self.get("/vault")
    get_vault_property = property(get_vault)

    def patch_vault(self, body):
        '''Alternate API call for PATCH /vault'''
        response = self.patch("/vault", body)
        return response
