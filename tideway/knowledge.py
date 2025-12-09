# -*- coding: utf-8 -*-

import tideway

appliance = tideway.main.Appliance

class Knowledge(appliance):
    '''Upload new TKUs and pattern modules.'''

    def get_knowledge(self):
        '''Get the current state of the appliance's knowledge, including TKU versions.'''
        return self.get("/knowledge")
    get_knowledge_property = property(get_knowledge)

    def get_knowledge_status(self):
        '''Get the current state of a knowledge upload.'''
        return self.get("/knowledge/status")

    get_knowledge_status_property = property(get_knowledge_status)

    def post_knowledge(self, filename, file, activate=True, allow_restart=False):
        '''Alternate API call for POST /knowledge/filename'''
        self.params['activate'] = activate
        self.params['allow_restart'] = allow_restart
        with open(file, "rb") as upload:
            files = {"file": upload}
            return self.post(
                "/knowledge/{}".format(filename),
                files=files,
                response="text/html",
            )

    def getKnowledgeTriggerPatterns(self, lookup_data_sources=None):
        '''Get a list of all knowledge trigger patterns.'''
        self.params['lookup_data_sources'] = lookup_data_sources
        response = self.get("/knowledge/trigger_patterns")
        return response
    get_knowledge_trigger_patterns = property(getKnowledgeTriggerPatterns)
