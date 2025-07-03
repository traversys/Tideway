# -*- coding: utf-8 -*-

import tideway

dr = tideway.discoRequests
appliance = tideway.main.Appliance

class Admin(appliance):
    '''Manage the BMC Discovery appliance.'''

    def baseline(self):
        '''Get a summary of the appliance status, and details of which baseline checks have passed or failed.'''
        response = dr.discoRequest(self, "/admin/baseline")
        return response
    get_admin_baseline = property(baseline)

    def admin(self):
        '''Get information about the appliance, like its version and versions of the installed packages.'''
        response = dr.discoRequest(self, "/admin/about")
        return response
    get_admin_about = property(admin)

    def licensing(self,content_type="text/plain"):
        '''Get the latest signed licensing report.'''
        if content_type == "csv":
            response = dr.discoRequest(self, "/admin/licensing/csv",response="application/zip")
        elif content_type == "raw":
            response = dr.discoRequest(self, "/admin/licensing/raw",response="application/zip")
        else:
            response = dr.discoRequest(self, "/admin/licensing",response=content_type)
        return response

    def instance(self):
        '''Get details about the appliance instance.'''
        response = dr.discoRequest(self, "/admin/instance")
        return response
    get_admin_instance = property(instance)

    def cluster(self):
        '''Get cluster configuration and status.'''
        response = dr.discoRequest(self, "/admin/cluster")
        return response
    get_admin_cluster = property(cluster)

    def organizations(self):
        '''Get configured organizations.'''
        response = dr.discoRequest(self, "/admin/organizations")
        return response
    get_admin_organizations = property(organizations)

    def preferences(self):
        '''Get global appliance preferences.'''
        response = dr.discoRequest(self, "/admin/preferences")
        return response
    get_admin_preferences = property(preferences)

    def builtin_reports(self):
        '''Get built-in report definitions.'''
        response = dr.discoRequest(self, "/admin/builtin_reports")
        return response
    get_admin_builtin_reports = property(builtin_reports)

    def custom_reports(self):
        '''Get custom report definitions.'''
        response = dr.discoRequest(self, "/admin/custom_reports")
        return response
    get_admin_custom_reports = property(custom_reports)

    def smtp(self):
        '''Get SMTP configuration.'''
        response = dr.discoRequest(self, "/admin/smtp")
        return response
    get_admin_smtp = property(smtp)
