# -*- coding: utf-8 -*-

import tideway

# Request helpers
dr = tideway.discoRequests
appliance = tideway.main.Appliance

class Security(appliance):
    '''Manage security settings and users.'''

    def get_security_ldap(self):
        '''Retrieve LDAP configuration.'''
        return dr.discoRequest(self, "/security/ldap")
    get_security_ldaps = property(get_security_ldap)

    def put_security_ldap(self, body):
        '''Replace LDAP configuration.'''
        return dr.discoPut(self, "/security/ldap", body)

    def patch_security_ldap(self, body):
        '''Update LDAP configuration.'''
        return dr.discoPatch(self, "/security/ldap", body)

    def get_security_group(self, group_name=None):
        '''Retrieve all groups or a specific group.'''
        if group_name:
            return dr.discoRequest(self, f"/security/groups/{group_name}")
        return dr.discoRequest(self, "/security/groups")
    get_security_groups = property(get_security_group)

    def post_security_group(self, body):
        '''Create a new group.'''
        return dr.discoPost(self, "/security/groups", body)

    def patch_security_group(self, group_name, body):
        '''Update a group.'''
        return dr.discoPatch(self, f"/security/groups/{group_name}", body)

    def delete_security_group(self, group_name):
        '''Delete a group.'''
        return dr.discoDelete(self, f"/security/groups/{group_name}")

    def get_security_permission(self, permission=None):
        '''Retrieve permissions or a specific permission set.'''
        if permission:
            return dr.discoRequest(self, f"/security/permissions/{permission}")
        return dr.discoRequest(self, "/security/permissions")
    get_security_permissions = property(get_security_permission)

    def get_security_user(self, username=None):
        '''Retrieve users or a specific user.'''
        if username:
            return dr.discoRequest(self, f"/security/users/{username}")
        return dr.discoRequest(self, "/security/users")
    get_security_users = property(get_security_user)

    def post_security_user(self, body):
        '''Create a new user.'''
        return dr.discoPost(self, "/security/users", body)

    def patch_security_user(self, username, body):
        '''Update a user.'''
        return dr.discoPatch(self, f"/security/users/{username}", body)

    def delete_security_user(self, username):
        '''Delete a user.'''
        return dr.discoDelete(self, f"/security/users/{username}")

    def post_security_token(self, body):
        '''Retrieve an authentication token for a user.'''
        return dr.discoPost(self, "/security/token", body)
