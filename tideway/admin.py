# -*- coding: utf-8 -*-

import tideway
import warnings

appliance = tideway.main.Appliance

class Admin(appliance):
    '''Manage the BMC Discovery appliance.'''

    def baseline(self):
        '''Get a summary of the appliance status, and details of which baseline checks have passed or failed.'''
        warnings.warn(
            "baseline() is deprecated; use get_admin_baseline instead.",
            DeprecationWarning,
        )
        return self.get("/admin/baseline")
    get_admin_baseline = property(baseline)

    def admin(self):
        '''Get information about the appliance, like its version and versions of the installed packages.'''
        warnings.warn(
            "admin() is deprecated; use get_admin_about instead.",
            DeprecationWarning,
        )
        return self.get("/admin/about")
    get_admin_about = property(admin)

    def licensing(self,content_type="text/plain"):
        '''Get the latest signed licensing report.'''
        warnings.warn(
            "licensing() is deprecated; use get_admin_licensing* helpers instead.",
            DeprecationWarning,
        )
        if content_type == "csv":
            response = self.get("/admin/licensing/csv", response="application/zip")
        elif content_type == "raw":
            response = self.get("/admin/licensing/raw", response="application/zip")
        else:
            response = self.get("/admin/licensing", response=content_type)
        return response

    def instance(self):
        '''Get details about the appliance instance.'''
        return self.get("/admin/instance")
    get_admin_instance = property(instance)

    def cluster(self):
        '''Get cluster configuration and status.'''
        return self.get("/admin/cluster")
    get_admin_cluster = property(cluster)

    def organizations(self):
        '''Get configured organizations.'''
        return self.get("/admin/organizations")
    get_admin_organizations = property(organizations)

    def preferences(self):
        '''Get global appliance preferences.'''
        return self.get("/admin/preferences")
    get_admin_preferences = property(preferences)

    def builtin_reports(self):
        '''Get built-in report definitions.'''
        return self.get("/admin/builtin_reports")
    get_admin_builtin_reports = property(builtin_reports)

    def custom_reports(self):
        '''Get custom report definitions.'''
        return self.get("/admin/custom_reports")
    get_admin_custom_reports = property(custom_reports)

    def smtp(self):
        '''Get SMTP configuration.'''
        return self.get("/admin/smtp")
    get_admin_smtp = property(smtp)
