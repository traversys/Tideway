# -*- coding: utf-8 -*-

import tideway

appliance = tideway.main.Appliance

class Security(appliance):
    '''Manage security settings and users.'''

    def get_security_ldap(self):
        '''Retrieve LDAP configuration.'''
        return self.get("/security/ldap")
    get_security_ldaps = property(get_security_ldap)

    def put_security_ldap(self, body):
        '''Replace LDAP configuration.'''
        return self.put("/security/ldap", body)

    def patch_security_ldap(self, body):
        '''Update LDAP configuration.'''
        return self.patch("/security/ldap", body)

    def get_security_group(self, group_name=None):
        '''Retrieve all groups or a specific group.'''
        if group_name:
            return self.get( f"/security/groups/{group_name}")
        return self.get("/security/groups")
    get_security_groups = property(get_security_group)

    def post_security_group(self, body):
        '''Create a new group.'''
        return self.post("/security/groups", body)

    def patch_security_group(self, group_name, body):
        '''Update a group.'''
        return self.patch( f"/security/groups/{group_name}", body)

    def delete_security_group(self, group_name):
        '''Delete a group.'''
        return self.delete( f"/security/groups/{group_name}")

    def get_security_permission(self, permission=None):
        '''Retrieve permissions or a specific permission set.'''
        if permission:
            return self.get( f"/security/permissions/{permission}")
        return self.get("/security/permissions")
    get_security_permissions = property(get_security_permission)

    def get_security_user(self, username=None):
        '''Retrieve users or a specific user.'''
        if username:
            return self.get( f"/security/users/{username}")
        return self.get("/security/users")
    get_security_users = property(get_security_user)

    def post_security_user(self, body):
        '''Create a new user.'''
        return self.post("/security/users", body)

    def patch_security_user(self, username, body):
        '''Update a user.'''
        return self.patch( f"/security/users/{username}", body)

    def delete_security_user(self, username):
        '''Delete a user.'''
        return self.delete( f"/security/users/{username}")

    def post_security_token(self, body):
        '''Retrieve an authentication token for a user.'''
        return self.post("/security/token", body)
