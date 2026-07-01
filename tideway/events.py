# -*- coding: utf-8 -*-

import tideway
appliance = tideway.main.Appliance

class Events(appliance):
    '''Push events.'''

    def post_events(self, body):
        '''An alternate API call for POST /events'''
        response = self.post("/events", body)
        return response
