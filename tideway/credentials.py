# -*- coding: utf-8 -*-

import tideway

appliance = tideway.main.Appliance

class Credentials(appliance):
    '''Manage credentials.'''

    def get_vault_credential_type(self, group=None, category=None):
        '''Altnernate API call for /vault/credential_types.'''
        self.params['group'] = group
        self.params['category'] = category
        return self.get("/vault/credential_types")
    get_vault_credential_types = property(get_vault_credential_type)

    def listCredentialTypes(self, group=None, category=None):
        '''Get a list of all credential types and filter by group and/or category.'''
        self.params['group'] = group
        self.params['category'] = category
        return self.get("/vault/credential_types")

    def get_vault_credential_type_name(self, cred_type_name):
        '''Altnernate API call for /vault/credential_types/cred_type_name.'''
        return self.get("/vault/credential_types/{}".format(cred_type_name))

    def credentialType(self, cred_type_name):
        '''Get the properties of a specific credential type.'''
        return self.get("/vault/credential_types/{}".format(cred_type_name))

    def get_vault_credential(self, cred_id=None):
        '''Altnernate API call for /vault/credentials.'''
        if cred_id:
            req = self.get("/vault/credentials/{}".format(cred_id))
        else:
            req = self.get("/vault/credentials")
        return req
    get_vault_credentials = property(get_vault_credential)

    def listCredentials(self, cred_id=None):
        '''Get a list of all credentials.'''
        if cred_id:
            response = self.get("/vault/credentials/{}".format(cred_id))
        else:
            response = self.get("/vault/credentials")
        return response

    def post_vault_credential(self, body):
        '''Altnernate API call for /vault/credentials.'''
        return self.post("/vault/credentials", body)

    def newCredential(self, body):
        '''Create a new credential.'''
        return self.post("/vault/credentials", body)

    def delete_vault_credential(self, cred_id):
        '''Altnernate API call for /vault/credentials.'''
        return self.delete("/vault/credentials/{}".format(cred_id))

    def deleteCredential(self, cred_id):
        '''Delete a credential.'''
        return self.delete("/vault/credentials/{}".format(cred_id))

    def patch_vault_credential(self, cred_id, body):
        '''Altnernate API call for /vault/credentials.'''
        return self.patch("/vault/credentials/{}".format(cred_id), body)

    def updateCredential(self, cred_id, body):
        '''Updates partial resources of a credential. Missing properties are left unchanged.'''
        return self.patch("/vault/credentials/{}".format(cred_id), body)

    def put_vault_credential(self, cred_id, body):
        '''Altnernate API call for /vault/credentials.'''
        return self.put("/vault/credentials/{}".format(cred_id), body)

    def replaceCredential(self, cred_id, body):
        '''Replaces a single credential. All required credential properties must be present. Optional properties that are missing will be reset to their defaults.'''
        return self.put("/vault/credentials/{}".format(cred_id), body)
