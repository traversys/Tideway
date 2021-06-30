# -*- coding: utf-8 -*-

import requests
import tideway

dr = tideway.discoRequests
appliance = tideway.main.Appliance

class Credentials(appliance):
    '''Manage credentials.'''

    def listCredentialTypes(self, group=None, category=None):
        '''Get a list of all credential types and filter by group and/or category.'''
        self.params['group'] = group
        self.params['category'] = category
        response = dr.discoRequest(self, "/vault/credential_types")
        return response

    def credentialType(self, cred_type_name):
        '''Get the properties of a specific credential type.'''
        response = dr.discoRequest(self, "/vault/credential_types/{}".format(cred_type_name))
        return response

    def listCredentials(self, cred_id=None):
        '''Get a list of all credentials.'''
        if cred_id:
            response = dr.discoRequest(self, "/vault/credentials/{}".format(cred_id))
        else:
            response = dr.discoRequest(self, "/vault/credentials")
        return response

    def newCredential(self, body):
        '''Create a new credential.'''
        response = dr.discoPost(self, "/vault/credentials", body)
        return response

    def deleteCredential(self, cred_id):
        '''Delete a credential.'''
        response = dr.discoDelete(self, "/vault/credentials/{}".format(cred_id))
        return response

    def updateCredential(self, cred_id, body):
        '''Updates partial resources of a credential. Missing properties are left unchanged.'''
        response = dr.discoPatch(self, "/vault/credentials/{}".format(cred_id), body)
        return response

    def replaceCredential(self, cred_id, body):
        '''Replaces a single credential. All required credential properties must be present. Optional properties that are missing will be reset to their defaults.'''
        response = dr.discoPut(self, "/vault/credentials/{}".format(cred_id), body)
        return response
