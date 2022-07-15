# -*- coding: utf-8 -*-

import tideway
import warnings
import json

dr = tideway.discoRequests
appliance = tideway.main.Appliance

class Data(appliance):
    '''Retrieve data from the model.'''

    def get_data_search(self, query, offset=None, results_id=None, format=None, limit = 100, delete = False):
        '''Alternate API call for GET /data/search.'''
        return Data.search(self, query, offset, results_id, format, limit, delete)

    def post_data_search(self, query, offset=None, results_id=None, format=None, limit = 100, delete = False):
        '''Alternate API call for POST /data/search.'''
        return Data.search(self, query, offset, results_id, format, limit, delete)

    def get_data_search_object(self, query, offset=None, results_id=None, format="object", limit = 100, delete = False):
        '''Alternate API call for GET /data/search?format=object.'''
        return Data.search(self, query, offset, results_id, format, limit, delete)
    
    def post_data_search_object(self, query, offset=None, results_id=None, format="object", limit = 100, delete = False):
        '''Alternate API call for POST /data/search?format=object'''
        return Data.search(self, query, offset, results_id, format, limit, delete)

    def get_data_search_tree(self, query, offset=None, results_id=None, format="tree", limit = 100, delete = False):
        '''Alternate API call for GET /data/search?format=tree.'''
        return Data.search(self, query, offset, results_id, format, limit, delete)
    
    def post_data_search_tree(self, query, offset=None, results_id=None, format="tree", limit = 100, delete = False):
        '''Alternate API call for POST /data/search?format=tree.'''
        return Data.search(self, query, offset, results_id, format, limit, delete)

    def search(self, query, offset=None, results_id=None, format=None, limit = 100, delete = False):
        '''Run a search query, receiving paginated results.'''
        self.params['offset'] = offset
        self.params['results_id'] = results_id
        self.params['format'] = format
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
        del query, offset, results_id, format, limit, delete
        return response

    def searchQuery(self, body, offset=None, results_id=None, format=None, limit = 100, delete = False):
        '''An alternative to GET /data/search, for search queries which are too long for urls.'''
        warnings.warn('JSON search body can be used with the search() function.', DeprecationWarning)
        return Data.search(self, body, offset, results_id, format, limit, delete)

    def search_bulk(self, query, format = None, limit = 100, delete = False):
        '''Performs a bulk search, will loop through paginated results until the limit is reached and return a JSON object.'''
        initial = Data.search(self, query, None, None, format, limit, delete)
        if initial.ok:
            init_results = initial.json()
            results = init_results[0]
            all_results = []
            if 'headings' in results:
                headings = results['headings']
                all_results.append(headings)
            for item in results['results']:
                all_results.append(item)
            if 'results_id' and 'next_offset' in results:
                total = init_results[0]['count']
                res_id = results['results_id']
                next_offset=results['next_offset']
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
            return json.loads(json.dumps(all_results))
        else:
            return initial

    def post_data_condition(self, body, offset=None, results_id=None, format=None, limit = 100, delete = False):
        '''Search using a condition, retrieving tabular data as arrays'''
        self.params['offset'] = offset
        self.params['results_id'] = results_id
        self.params['format'] = format
        self.params['delete'] = delete
        self.params['limit'] = limit
        response = dr.discoPost(self, "/data/condition", body)
        return response

    def post_data_condition_param_values(self, body):
        '''Get possible parameter values for a condition'''
        response = dr.discoPost(self, "/data/condition/param_values", body)
        return response

    def get_data_condition_template(self, template_id=None):
        '''Get a list of all templates'''
        if template_id:
            req = dr.discoRequest(self, "/data/condition/templates/{}".format(template_id))
        else:
            req = dr.discoRequest(self, "/data/condition/templates")
        return req
    get_data_condition_templates = property(get_data_condition_template)

    def post_data_candidate(self, body):
        '''Alternate API call for POST /data/candidate.'''
        response = dr.discoPost(self, "/data/candidate", body)
        return response

    def best_candidate(self, body):
        '''
            The node object of the best candidate based on the provided parameters.
        '''
        response = dr.discoPost(self, "/data/candidate", body)
        return response

    def post_data_candidates(self, body):
        '''Alternate API call for POST /data/candidates.'''
        response = dr.discoPost(self, "/data/candidates", body)
        return response

    def top_candidates(self, body):
        '''
            Enter parameters to identify a device, the response is a list of
            candidate nodes ordered by descending score.
        '''
        response = dr.discoPost(self, "/data/candidates", body)
        return response

    def get_data_nodes(self, node_id, relationships=False, traverse=None, flags=None, attributes=None):
        '''Alternate API call for /data/nodes/node_id'''
        self.params['traverse'] = traverse
        self.params['flags'] = flags
        self.params['attributes'] = attributes
        if relationships:
            response = dr.discoRequest(self, "/data/nodes/{}?relationships=true".format(node_id))
        else:
            response = dr.discoRequest(self, "/data/nodes/{}".format(node_id))
        return response

    def nodeLookup(self, node_id, relationships=False, traverse=None, flags=None, attributes=None):
        '''Get the state of a node with specified id.'''
        self.params['traverse'] = traverse
        self.params['flags'] = flags
        self.params['attributes'] = attributes
        if relationships:
            response = dr.discoRequest(self, "/data/nodes/{}?relationships=true".format(node_id))
        else:
            response = dr.discoRequest(self, "/data/nodes/{}".format(node_id))
        return response

    def get_data_nodes_graph(self, node_id, focus="sofware-connected", apply_rules=True):
        '''Alternate API call for /data/nodes/node_id/graph'''
        self.params['focus'] = focus
        self.params['apply_rules'] = apply_rules
        self.params['complete'] = False
        response = dr.discoRequest(self, "/data/nodes/{}/graph".format(node_id))
        return response

    def graphNode(self, node_id, focus="sofware-connected", apply_rules=True):
        '''Graph data represents a set of nodes and relationships that are associated to the given node.'''
        self.params['focus'] = focus
        self.params['apply_rules'] = apply_rules
        response = dr.discoRequest(self, "/data/nodes/{}/graph".format(node_id))
        return response

    def get_data_kinds(self, kind, offset=None, results_id=None, format=None, limit = 100, delete = False):
        '''Alternate API call for /data/kinds.'''
        self.params['offset'] = offset
        self.params['results_id'] = results_id
        self.params['format'] = format
        self.params['limit'] = limit
        self.params['delete'] = delete
        response = dr.discoRequest(self, "/data/kinds/{}".format(kind))
        return response

    def lookupNodeKind(self, kind, offset=None, results_id=None, format=None, limit = 100, delete = False):
        '''Finds all nodes of a specified node kind.'''
        self.params['offset'] = offset
        self.params['results_id'] = results_id
        self.params['format'] = format
        self.params['limit'] = limit
        self.params['delete'] = delete
        response = dr.discoRequest(self, "/data/kinds/{}".format(kind))
        return response

    def partitions(self):
        '''Get names and ids of partitions.'''
        response = dr.discoRequest(self, "/data/partitions")
        return response
    get_data_partitions = property(partitions)

    def post_data_partitions(self, body):
        '''Create a partition.'''
        response = dr.discoPost(self, "/data/partitions", body)
        return response

    def post_data_import(self, body):
        '''Alternate API call for /data/import.'''
        response = dr.discoPost(self, "/data/import", body)
        return response

    def twImport(self, body):
        '''
            Imports data. Returns the import UUID.
        '''
        response = dr.discoPost(self, "/data/import", body)
        return response

    def post_data_write(self, body):
        '''Alternate API call for /data/write.'''
        response = dr.discoPost(self, "/data/write", body)
        return response

    def twWrite(self, body):
        '''
            Perform arbitrary write operations.
        '''
        response = dr.discoPost(self, "/data/write", body)
        return response
