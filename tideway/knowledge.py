# -*- coding: utf-8 -*-

import tideway
import warnings

dr = tideway.discoRequests
appliance = tideway.main.Appliance

class Knowledge(appliance):
    '''Upload new TKUs and pattern modules.'''

    def get_knowledge(self):
        '''Get the current state of the appliance's knowledge, including TKU versions.'''
        return dr.discoRequest(self, "/knowledge")

    def getKnowledgeManagement(self):
        '''Get the current state of the appliance's knowledge, including TKU versions.'''
        warnings.warn(
            "getKnowledgeManagement() is deprecated; use get_knowledge() instead.",
            DeprecationWarning,
        )
        return self.get_knowledge()
    get_knowledge_property = property(get_knowledge)

    def getUploadStatus(self):
        '''Get the current state of a knowledge upload.'''
        warnings.warn(
            "getUploadStatus() is deprecated; use get_knowledge_status() instead.",
            DeprecationWarning,
        )
        return self.get_knowledge_status()

    def get_knowledge_status(self):
        '''Get the current state of a knowledge upload.'''
        return dr.discoRequest(self, "/knowledge/status")

    get_knowledge_status_property = property(get_knowledge_status)

    def post_knowledge(self, filename, file, activate=True, allow_restart=False):
        '''Alternate API call for POST /knowledge/filename'''
        self.params['activate'] = activate
        self.params['allow_restart'] = allow_restart
        response = dr.filePost(self, "/knowledge/{}".format(filename), file)
        return response

    def uploadKnowledge(self, filename, file, activate=True, allow_restart=False):
        '''Upload a TKU or pattern module to the appliance.'''
        warnings.warn(
            "uploadKnowledge() is deprecated; use post_knowledge() instead.",
            DeprecationWarning,
        )
        return self.post_knowledge(filename, file, activate, allow_restart)

    def getKnowledgeTriggerPatterns(self, lookup_data_sources=None):
        '''Get a list of all knowledge trigger patterns.'''
        self.params['lookup_data_sources'] = lookup_data_sources
        response = dr.discoRequest(self, "/knowledge/trigger_patterns")
        return response
    get_knowledge_trigger_patterns = property(getKnowledgeTriggerPatterns)
