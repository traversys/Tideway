# -*- coding: utf-8 -*-

import requests
import tideway

dr = tideway.discoRequests
appliance = tideway.main.Appliance

class Events(appliance):
    '''Push events.'''

    def status(self, body):
        '''
            Returns a unique ID if the event has been recorded, otherwise an
            empty string is returned e.g. if the event source has been disabled.
        '''
        response = dr.discoPost(self, "/events", body)
        return response
