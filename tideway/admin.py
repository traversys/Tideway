# -*- coding: utf-8 -*-

import tideway

appliance = tideway.main.Appliance

class Admin(appliance):
    '''Manage the BMC Discovery appliance.'''

    def get_admin_baseline(self):
        '''Get a summary of the appliance status, and details of which baseline checks have passed or failed.'''
        return self.get("/admin/baseline")

    def get_admin_about(self):
        '''Get information about the appliance, like its version and versions of the installed packages.'''
        return self.get("/admin/about")

    def get_admin_licensing(self, content_type="text/plain"):
        '''Get the latest signed licensing report.'''
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

    def cluster(self):
        '''Get cluster configuration and status.'''
        return self.get("/admin/cluster")

    def organizations(self):
        '''Get configured organizations.'''
        return self.get("/admin/organizations")

    def preferences(self):
        '''Get global appliance preferences.'''
        return self.get("/admin/preferences")

    def builtin_reports(self):
        '''Get built-in report definitions.'''
        return self.get("/admin/builtin_reports")

    def custom_reports(self):
        '''Get custom report definitions.'''
        return self.get("/admin/custom_reports")

    def smtp(self):
        '''Get SMTP configuration.'''
        return self.get("/admin/smtp")
