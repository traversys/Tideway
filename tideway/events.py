# -*- coding: utf-8 -*-

import tideway

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
        response = dr.discoPost(self, "/events", body)
        return response
