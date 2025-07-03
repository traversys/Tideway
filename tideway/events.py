# -*- coding: utf-8 -*-

import tideway
import warnings

dr = tideway.discoRequests
appliance = tideway.main.Appliance

class Events(appliance):
    '''Push events.'''

    def post_events(self, body):
        '''An alternate API call for POST /events'''
        response = dr.discoPost(self, "/events", body)
        return response

    def status(self, body):
        '''
            Returns a unique ID if the event has been recorded, otherwise an
            empty string is returned e.g. if the event source has been disabled.
        '''
        warnings.warn(
            "status() is deprecated; use post_events() instead.",
            DeprecationWarning,
        )
        return self.post_events(body)
