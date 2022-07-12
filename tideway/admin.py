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
