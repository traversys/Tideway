# -*- coding: utf-8 -*-

import tideway

dr = tideway.discoRequests
appliance = tideway.main.Appliance

class Kerberos(appliance):
    '''Manage Kerberos resources.'''

    def get_vault_kerberos_realm(self, realm_name=None):
        '''Retrieve all or specific realm.'''
        if realm_name:
            req = dr.discoRequest(self, "/vault/kerberos/realms/{}".format(realm_name))
        else:
            req = dr.discoRequest(self, "/vault/kerberos/realms")
        return req
    get_vault_kerberos_realms = property(get_vault_kerberos_realm)

    def delete_vault_kerberos_realm(self, realm_name):
        '''Delete a realm.'''
        req = dr.discoDelete(self, "/vault/kerberos/realms/{}".format(realm_name))
        return req

    def patch_vault_kerberos_realm(self, realm_name, body):
        '''Update a Kerberos realm.'''
        req = dr.discoPatch(self, "/vault/kerberos/realms/{}".format(realm_name), body)
        return req

    def post_vault_kerberos_realm(self, realm_name, body, test=False):
        '''Create a realm and Test user credentials by attempting to acquire a new Kerberos Ticket Granting Ticket (TGT)'''
        req = dr.discoPost(self, "/vault/kerberos/realms/{}".format(realm_name), body)
        if test:
            req = dr.discoPost(self, "/vault/kerberos/realms/{}/test".format(realm_name), body)
        return req

    def get_vault_kerberos_keytabs(self, realm_name):
        '''List users with a Kerberos keytab file'''
        req = dr.discoRequest(self, "/vault/kerberos/realms/{}/keytabs".format(realm_name))
        return req

    def post_vault_kerberos_keytab(self, realm_name, username, keytab):
        '''Upload a Kerberos keytab file'''
        # Not Tested
        req = dr.keytabPost(self, "/vault/kerberos/realms/{}/keytabs".format(realm_name), keytab, username)
        return req

    def delete_vault_kerberos_keytab(self, realm_name, username):
        '''Delete a keytab file'''
        # Not Tested
        req = dr.discoDelete(self, "/vault/kerberos/realms/{}/keytabs/{}".format(realm_name, username))
        return req

    def get_vault_kerberos_ccaches(self, realm_name):
        '''List users with a Kerberos credential cache file.'''
        req = dr.discoRequest(self, "/vault/kerberos/realms/{}/ccaches".format(realm_name))
        return req

    def post_vault_kerberos_ccache(self, realm_name, username, ccache):
        '''Upload a Kerberos credential cache file'''
        # Not Tested
        req = dr.keytabPost(self, "/vault/kerberos/realms/{}/ccaches".format(realm_name), ccache, username)
        return req

    def delete_vault_kerberos_ccache(self, realm_name, username):
        '''Delete a credential cache file'''
        req = dr.discoDelete(self, "/vault/kerberos/realms/{}/ccaches/{}".format(realm_name, username))
        return req