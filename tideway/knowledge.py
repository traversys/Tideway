# -*- coding: utf-8 -*-

import tideway

dr = tideway.discoRequests
appliance = tideway.main.Appliance

class Knowledge(appliance):
    '''Upload new TKUs and pattern modules.'''

    def getKnowledgeManagement(self):
        '''Get the current state of the appliance's knowledge, including TKU versions.'''
        response = dr.discoRequest(self, "/knowledge")
        return response
    get_knowledge = property(getKnowledgeManagement)

    def getUploadStatus(self):
        '''Get the current state of a knowledge upload.'''
        response = dr.discoRequest(self, "/knowledge/status")
        return response
    get_knowledge_status = property(getUploadStatus)

    def post_knowledge(self, filename, file, activate=True, allow_restart=False):
        '''Alternate API call for POST /knowledge/filename'''
        self.params['activate'] = activate
        self.params['allow_restart'] = allow_restart
        response = dr.filePost(self, "/knowledge/{}".format(filename), file)
        return response

    def uploadKnowledge(self, filename, file, activate=True, allow_restart=False):
        '''Upload a TKU or pattern module to the appliance.'''
        self.params['activate'] = activate
        self.params['allow_restart'] = allow_restart
        response = dr.filePost(self, "/knowledge/{}".format(filename), file)
        return response
