# -*- coding: utf-8 -*-

import tideway

dr = tideway.discoRequests
appliance = tideway.main.Appliance

class Credentials(appliance):
    '''Manage credentials.'''

    def get_vault_credential_type(self, group=None, category=None):
        '''Altnernate API call for /vault/credential_types.'''
        self.params['group'] = group
        self.params['category'] = category
        req = dr.discoRequest(self, "/vault/credential_types")
        return req
    get_vault_credential_types = property(get_vault_credential_type)

    def listCredentialTypes(self, group=None, category=None):
        '''Get a list of all credential types and filter by group and/or category.'''
        self.params['group'] = group
        self.params['category'] = category
        response = dr.discoRequest(self, "/vault/credential_types")
        return response

    def get_vault_credential_type_name(self, cred_type_name):
        '''Altnernate API call for /vault/credential_types/cred_type_name.'''
        req = dr.discoRequest(self, "/vault/credential_types/{}".format(cred_type_name))
        return req

    def credentialType(self, cred_type_name):
        '''Get the properties of a specific credential type.'''
        response = dr.discoRequest(self, "/vault/credential_types/{}".format(cred_type_name))
        return response

    def get_vault_credential(self, cred_id=None):
        '''Altnernate API call for /vault/credentials.'''
        if cred_id:
            req = dr.discoRequest(self, "/vault/credentials/{}".format(cred_id))
        else:
            req = dr.discoRequest(self, "/vault/credentials")
        return req
    get_vault_credentials = property(get_vault_credential)

    def listCredentials(self, cred_id=None):
        '''Get a list of all credentials.'''
        if cred_id:
            response = dr.discoRequest(self, "/vault/credentials/{}".format(cred_id))
        else:
            response = dr.discoRequest(self, "/vault/credentials")
        return response

    def post_vault_credential(self, body):
        '''Altnernate API call for /vault/credentials.'''
        req = dr.discoPost(self, "/vault/credentials", body)
        return req

    def newCredential(self, body):
        '''Create a new credential.'''
        response = dr.discoPost(self, "/vault/credentials", body)
        return response

    def delete_vault_credential(self, cred_id):
        '''Altnernate API call for /vault/credentials.'''
        req = dr.discoDelete(self, "/vault/credentials/{}".format(cred_id))
        return req

    def deleteCredential(self, cred_id):
        '''Delete a credential.'''
        response = dr.discoDelete(self, "/vault/credentials/{}".format(cred_id))
        return response

    def patch_vault_credential(self, cred_id, body):
        '''Altnernate API call for /vault/credentials.'''
        req = dr.discoPatch(self, "/vault/credentials/{}".format(cred_id), body)
        return req

    def updateCredential(self, cred_id, body):
        '''Updates partial resources of a credential. Missing properties are left unchanged.'''
        response = dr.discoPatch(self, "/vault/credentials/{}".format(cred_id), body)
        return response

    def put_vault_credential(self, cred_id, body):
        '''Altnernate API call for /vault/credentials.'''
        req = dr.discoPut(self, "/vault/credentials/{}".format(cred_id), body)
        return req

    def replaceCredential(self, cred_id, body):
        '''Replaces a single credential. All required credential properties must be present. Optional properties that are missing will be reset to their defaults.'''
        response = dr.discoPut(self, "/vault/credentials/{}".format(cred_id), body)
        return response
