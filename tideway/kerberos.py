# -*- coding: utf-8 -*-

import tideway

appliance = tideway.main.Appliance

class Kerberos(appliance):
    '''Manage Kerberos resources.'''

    def get_vault_kerberos_realm(self, realm_name=None):
        '''Retrieve all or specific realm.'''
        if realm_name:
            req = self.get("/vault/kerberos/realms/{}".format(realm_name))
        else:
            req = self.get("/vault/kerberos/realms")
        return req
    get_vault_kerberos_realms = property(get_vault_kerberos_realm)

    def delete_vault_kerberos_realm(self, realm_name):
        '''Delete a realm.'''
        req = self.delete("/vault/kerberos/realms/{}".format(realm_name))
        return req

    def patch_vault_kerberos_realm(self, realm_name, body):
        '''Update a Kerberos realm.'''
        req = self.patch("/vault/kerberos/realms/{}".format(realm_name), body)
        return req

    def post_vault_kerberos_realm(self, realm_name, body, test=False):
        '''Create a realm and Test user credentials by attempting to acquire a new Kerberos Ticket Granting Ticket (TGT)'''
        req = self.post("/vault/kerberos/realms/{}".format(realm_name), body)
        if test:
            req = self.post("/vault/kerberos/realms/{}/test".format(realm_name), body)
        return req

    def get_vault_kerberos_keytabs(self, realm_name):
        '''List users with a Kerberos keytab file'''
        req = self.get("/vault/kerberos/realms/{}/keytabs".format(realm_name))
        return req

    def post_vault_kerberos_keytab(self, realm_name, username, keytab):
        '''Upload a Kerberos keytab file'''
        # Not Tested
        with open(keytab, "rb") as kf:
            files = {"keytab": kf, "username": (None, username)}
            return self.post(
                "/vault/kerberos/realms/{}/keytabs".format(realm_name),
                files=files,
                response="application/json",
                content_type="multipart/form-data",
            )

    def delete_vault_kerberos_keytab(self, realm_name, username):
        '''Delete a keytab file'''
        # Not Tested
        req = self.delete("/vault/kerberos/realms/{}/keytabs/{}".format(realm_name, username))
        return req

    def get_vault_kerberos_ccaches(self, realm_name):
        '''List users with a Kerberos credential cache file.'''
        req = self.get("/vault/kerberos/realms/{}/ccaches".format(realm_name))
        return req

    def post_vault_kerberos_ccache(self, realm_name, username, ccache):
        '''Upload a Kerberos credential cache file'''
        # Not Tested
        with open(ccache, "rb") as cache_file:
            files = {"keytab": cache_file, "username": (None, username)}
            return self.post(
                "/vault/kerberos/realms/{}/ccaches".format(realm_name),
                files=files,
                response="application/json",
                content_type="multipart/form-data",
            )

    def delete_vault_kerberos_ccache(self, realm_name, username):
        '''Delete a credential cache file'''
        req = self.delete("/vault/kerberos/realms/{}/ccaches/{}".format(realm_name, username))
        return req
