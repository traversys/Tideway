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

    def _search_once(self, query, offset=None, results_id=None, format=None, limit=100, delete=False):
        """Internal helper for single page search request."""
        self.params['offset'] = offset
        self.params['results_id'] = results_id
        self.params['format'] = format
        self.params['delete'] = delete
        self.params['limit'] = limit
        try:
            body = query
            _ = query["query"]
            response = dr.discoPost(self, "/data/search", body)
        except Exception:
            self.params['query'] = query
            response = dr.discoRequest(self, "/data/search")
        return response

    def _search_all(self, query, format=None, limit=100, delete=False, record_limit=None, call_limit=None):
        """Retrieve all paginated search results respecting limits."""
        initial = self._search_once(query, None, None, format, limit, delete)
        if not initial.ok:
            return initial

        init_results = initial.json()
        results = init_results[0]
        all_results = []
        if 'headings' in results:
            headings = results['headings']
            all_results.append(headings)
        for item in results['results']:
            all_results.append(item)
            if record_limit is not None and len(all_results) - ('headings' in results) >= record_limit:
                return json.loads(json.dumps(all_results))

        if 'results_id' in results and 'next_offset' in results:
            res_id = results['results_id']
            next_offset = results['next_offset']
            calls_made = 0
            while True:
                if call_limit is not None and calls_made >= call_limit:
                    break
                s = self._search_once(query, next_offset, res_id, format, limit, delete)
                if not s.ok:
                    return s
                json_results = s.json()
                records = json_results[0]['results']
                for item in records:
                    all_results.append(item)
                    if record_limit is not None and len(all_results) - ('headings' in results) >= record_limit:
                        return json.loads(json.dumps(all_results))
                calls_made += 1
                if 'next_offset' in json_results[0]:
                    next_offset = json_results[0]['next_offset']
                else:
                    break
        return json.loads(json.dumps(all_results))

    def search(self, query, offset=None, results_id=None, format=None, limit=100, delete=False, bulk=True, record_limit=None, call_limit=None):
        """Run a search query. By default all results are returned."""
        if offset is not None or results_id is not None or not bulk:
            response = self._search_once(query, offset, results_id, format, limit, delete)
            return response
        return self._search_all(query, format, limit, delete, record_limit, call_limit)

    def searchQuery(self, body, offset=None, results_id=None, format=None, limit = 100, delete = False):
        '''An alternative to GET /data/search, for search queries which are too long for urls.'''
        warnings.warn(
            "searchQuery() is deprecated; use search() instead.",
            DeprecationWarning,
        )
        return Data.search(self, body, offset, results_id, format, limit, delete)

    def search_bulk(self, query, format=None, limit=100, delete=False, record_limit=None, call_limit=None):
        '''Performs a bulk search, looping through paginated results.'''
        return self._search_all(query, format, limit, delete, record_limit, call_limit)

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
        '''Get a template or a list of all templates.'''
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
        warnings.warn(
            "best_candidate() is deprecated; use post_data_candidate() instead.",
            DeprecationWarning,
        )
        return self.post_data_candidate(body)

    def post_data_candidates(self, body):
        '''Alternate API call for POST /data/candidates.'''
        response = dr.discoPost(self, "/data/candidates", body)
        return response

    def top_candidates(self, body):
        '''
            Enter parameters to identify a device, the response is a list of
            candidate nodes ordered by descending score.
        '''
        warnings.warn(
            "top_candidates() is deprecated; use post_data_candidates() instead.",
            DeprecationWarning,
        )
        return self.post_data_candidates(body)

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
        warnings.warn(
            "nodeLookup() is deprecated; use get_data_nodes() instead.",
            DeprecationWarning,
        )
        return self.get_data_nodes(
            node_id,
            relationships=relationships,
            traverse=traverse,
            flags=flags,
            attributes=attributes,
        )

    def get_data_nodes_graph(self, node_id, focus="software-connected", apply_rules=True, complete=False):
        '''Alternate API call for /data/nodes/node_id/graph'''
        self.params['focus'] = focus
        self.params['apply_rules'] = apply_rules
        self.params['complete'] = complete
        response = dr.discoRequest(self, "/data/nodes/{}/graph".format(node_id))
        return response

    def graphNode(self, node_id, focus="software-connected", apply_rules=True):
        '''Graph data represents a set of nodes and relationships that are associated to the given node.'''
        warnings.warn(
            "graphNode() is deprecated; use get_data_nodes_graph() instead.",
            DeprecationWarning,
        )
        return self.get_data_nodes_graph(
            node_id,
            focus=focus,
            apply_rules=apply_rules,
            complete=False,
        )

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
        warnings.warn(
            "lookupNodeKind() is deprecated; use get_data_kinds() instead.",
            DeprecationWarning,
        )
        return self.get_data_kinds(
            kind,
            offset=offset,
            results_id=results_id,
            format=format,
            limit=limit,
            delete=delete,
        )

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
        warnings.warn(
            "twImport() is deprecated; use post_data_import() instead.",
            DeprecationWarning,
        )
        return self.post_data_import(body)

    def post_data_write(self, body):
        '''Alternate API call for /data/write.'''
        response = dr.discoPost(self, "/data/write", body)
        return response

    def twWrite(self, body):
        '''
            Perform arbitrary write operations.
        '''
        warnings.warn(
            "twWrite() is deprecated; use post_data_write() instead.",
            DeprecationWarning,
        )
        return self.post_data_write(body)

    def get_data_condition_params(self):
        '''Retrieve the list of available condition parameters.'''
        response = dr.discoRequest(self, "/data/condition/params")
        return response

    def post_data_import_graph(self, body):
        '''Import graph data and return the import UUID.'''
        response = dr.discoPost(self, "/data/import/graph", body)
        return response

    def get_data_external_consumer(self, consumer_name=None, path=None):
        '''Retrieve external consumer information.'''
        endpoint = "/data/external_consumers"
        if consumer_name:
            endpoint += f"/{consumer_name}"
            if path:
                endpoint += f"/{path}"
        response = dr.discoRequest(self, endpoint)
        return response
    get_data_external_consumers = property(get_data_external_consumer)

    def post_data_external_consumer(self, body, consumer_name=None, path=None):
        '''Create or interact with an external consumer resource.'''
        endpoint = "/data/external_consumers"
        if consumer_name:
            endpoint += f"/{consumer_name}"
            if path:
                endpoint += f"/{path}"
        response = dr.discoPost(self, endpoint, body)
        return response

    def patch_data_external_consumer(self, consumer_name, body, path=None):
        '''Update an external consumer resource.'''
        endpoint = f"/data/external_consumers/{consumer_name}"
        if path:
            endpoint += f"/{path}"
        response = dr.discoPatch(self, endpoint, body)
        return response

    def delete_data_external_consumer(self, consumer_name, path=None):
        '''Delete an external consumer resource.'''
        endpoint = f"/data/external_consumers/{consumer_name}"
        if path:
            endpoint += f"/{path}"
        response = dr.discoDelete(self, endpoint)
        return response

    def get_data_kinds_values(self, kind, attribute, offset=None, results_id=None, format=None, limit=100, delete=False):
        '''Retrieve values for an attribute of a node kind.'''
        self.params['offset'] = offset
        self.params['results_id'] = results_id
        self.params['format'] = format
        self.params['limit'] = limit
        self.params['delete'] = delete
        endpoint = f"/data/kinds/{kind}/values/{attribute}"
        response = dr.discoRequest(self, endpoint)
        return response
