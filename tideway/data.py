# -*- coding: utf-8 -*-

import requests
import tideway

dr = tideway.discoRequests
appliance = tideway.main.Appliance

class Data(appliance):
    '''Retrieve data from the model.'''

    def search(self, query, offset=None, results_id=None, format=None):
        '''Run a search query, receiving paginated results.'''
        self.params['query'] = query
        if offset:
            self.params['offset'] = offset
        if results_id:
            self.params['results_id'] = results_id
        if format:
            self.params['format'] = format
        response = dr.discoRequest(self, "/data/search")
        return response

    def searchQuery(self, body, offset=None, results_id=None, format=None):
        '''An alternative to GET /data/search, for search queries which are too long for urls.'''
        if format:
            self.params['format'] = format
        response = dr.discoPost(self, "/data/search", body)
        return response

    def candidate(self, body):
        '''
            The node object of the best candidate based on the provided
            parameters.
        '''
        response = dr.discoPost(self, "/data/candidate", body)
        return response

    def candidates(self, body):
        '''
            Enter parameters to identify a device, the response is a list of
            candidate nodes ordered by descending score.
        '''
        response = dr.discoPost(self, "/data/candidate", body)
        return response

    def nodeLookup(self, node_id, relationships=False, traverse=None, flags=None, attributes=None):
        '''Get the state of a node with specified id.'''
        if traverse:
            self.params['traverse'] = traverse
            if flags:
                self.params['flags'] = flags
        if offset:
            self.params['offset'] = offset
        if results_id:
            self.params['results_id'] = results_id
        if format:
            self.params['format'] = format
        if attributes:
            self.params['attributes'] = attributes
        if relationships:
            response = dr.discoRequest(self, "/data/nodes/{}?relationships=true".format(node_id))
        else:
            response = dr.discoRequest(self, "/data/nodes/{}".format(node_id))
        return response

    def graphNode(self, node_id, focus="sofware-connected", apply_rules=True):
        '''Graph data represents a set of nodes and relationships that are associated to the given node.'''
        if focus:
            self.params['focus'] = focus
        if apply_rules:
            self.params['apply_rules'] = apply_rules
        response = dr.discoRequest(self, "/data/nodes/{}/graph".format(node_id))
        return response

    def lookupNodeKind(self, kind, offset=None, results_id=None, format=None):
        '''Finds all nodes of a specified node kind.'''
        if offset:
            self.params['offset'] = offset
        if results_id:
            self.params['results_id'] = results_id
        if format:
            self.params['format'] = format
        response = dr.discoRequest(self, "/data/kinds/{}".format(kind))
        return response

    def partitions(self):
        '''Get names and ids of partitions.'''
        response = dr.discoRequest(self, "/data/partitions")
        return response

    def twImport(self, body):
        '''
            Imports data. Returns the import UUID.
        '''
        response = dr.discoPost(self, "/data/import", body)
        return response

    def twWrite(self, body):
        '''
            Perform arbitrary write operations.
        '''
        response = dr.discoPost(self, "/data/write", body)
        return response
