# -*- coding: utf-8 -*-

import requests
import tideway
import warnings
import json

dr = tideway.discoRequests
appliance = tideway.main.Appliance

class Data(appliance):
    '''Retrieve data from the model.'''

    def search(self, query, offset=None, results_id=None, format=None, limit = 100, delete = False):
        '''Run a search query, receiving paginated results.'''
        if offset:
            self.params['offset'] = offset
        if results_id:
            self.params['results_id'] = results_id
        if format:
            self.params['format'] = format
        if delete:
            self.params['delete'] = delete
        self.params['limit'] = limit
        try:
            q = query["query"]
            body = query
            response = dr.discoPost(self, "/data/search", body)
        except:
            q = False
            self.params['query'] = query
            response = dr.discoRequest(self, "/data/search")
        return response

    def searchQuery(self, body, offset=None, results_id=None, format=None, limit = 100, delete = False):
        '''An alternative to GET /data/search, for search queries which are too long for urls.'''
        warnings.warn('JSON search body can be used with the search() function.', DeprecationWarning)
        return Data.search(self, body, offset, results_id, format, limit, delete)

    def search_bulk(self, query, format=None, limit = 100, delete = False):
        '''Performs a bulk search, will loop through paginated results until the limit is reached and return a JSON object.'''
        initial = Data.search(self, query, None, None, format, limit, delete)
        init_results = initial.json()
        res_id = init_results[0]['results_id']
        all_results = []
        for item in init_results[0]['results']:
            all_results.append(item)
        total = init_results[0]['count']
        next_offset=init_results[0]['next_offset']
        total = int(total / next_offset)
        for count in range(0,total):
            s = Data.search(self, query, next_offset, res_id, format, limit, delete)
            json_results = s.json()
            records = json_results[0]['results']
            for item in records:
                all_results.append(item)
            if 'next_offset' in json_results[0]:
                next_offset=json_results[0]['next_offset']
            else:
                break
        response = json.loads(json.dumps(all_results))
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

    def lookupNodeKind(self, kind, offset=None, results_id=None, format=None, limit = 100, delete = False):
        '''Finds all nodes of a specified node kind.'''
        if offset:
            self.params['offset'] = offset
        if results_id:
            self.params['results_id'] = results_id
        if format:
            self.params['format'] = format
        self.params['limit'] = limit
        self.params['delete'] = delete
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
