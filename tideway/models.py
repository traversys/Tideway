# -*- coding: utf-8 -*-

import tideway

dr = tideway.discoRequests
appliance = tideway.main.Appliance

class Models(appliance):
    '''Manage service and application models.'''

    def get_model(self,name=None,type=None,kind=None,published=None,review_suggested=None,version=None,favorite=None,compatibility=None,results_id=None,delete=False):
        '''Get model definitions.'''
        if name:
            self.params['name'] = name
        if type:
            self.params['type'] = type
        if kind:
            self.params['kind'] = kind
        if published:
            self.params['published'] = published
        if review_suggested:
            self.params['review_suggested'] = review_suggested
        if version:
            self.params['version'] = version
        if favorite:
            self.params['favorite'] = favorite
        if compatibility:
            self.params['compatibility'] = compatibility
        if results_id:
            self.params['results_id'] = results_id
        if delete:
            self.params['delete'] = delete
        response = dr.discoRequest(self, "/models")
        return response
    get_models = property(get_model)

    def post_model(self, body):
        '''Create a new model.'''
        response = dr.discoPost(self, "/models", body)
        return response

    def post_model_multi(self, body):
        '''Manipulate multiple models in a single request.'''
        response = dr.discoPost(self, "/models/multi", body)
        return response

    def delete_model(self, key):
        '''Delete a model.'''
        response = dr.discoDelete(self, "/models/{}".format(key))
        return response

    def get_model_key(self, key):
        '''Get model definition for the specified key.'''
        req = dr.discoRequest(self, "/models/{}".format(key))
        return req

    def patch_model(self, key, body):
        '''Modify a model.'''
        response = dr.discoPatch(self, "/models/{}".format(key), body)
        return response

    def get_model_topology(self, key, attributes=None):
        '''Get topology for the model definition specified by key.'''
        if attributes:
            self.params['attributes']=attributes
        req = dr.discoRequest(self, "/models/{}/topology".format(key))
        return req

    def get_model_nodecount(self, key):
        '''Get node count for the model definition specified by key.'''
        req = dr.discoRequest(self, "/models/{}/nodecount".format(key))
        return req

    def get_model_nodes(self, key, format=None, limit=100, results_id=None, delete=False, kind=None):
        '''Get nodes for the model definition specified by key.'''
        if format:
            self.params['format'] = format
        if results_id:
            self.params['results_id'] = results_id    
        self.params['limit'] = limit
        self.params['delete'] = delete
        if kind:
            response = dr.discoRequest(self, "/models/{}/nodes/{}".format(key,kind))
        else:
            response = dr.discoRequest(self, "/models/{}/nodes".format(key))
        return response

    def delete_model_by_node_id(self, node_id):
        '''Delete a model.'''
        response = dr.discoDelete(self, "/models/by_node_id/{}".format(node_id))
        return response

    def get_model_by_node_id(self, node_id, expand_related=None):
        '''Get model definition for the specified node id.'''
        if expand_related:
            self.params['expand_related'] = expand_related
        response = dr.discoRequest(self, "/models/by_node_id/{}".format(node_id))
        return response

    def patch_model_by_node_id(self, node_id, body):
        '''Modify a model.'''
        response = dr.discoPatch(self, "/models/by_node_id/{}".format(node_id), body)
        return response

    def get_topology_by_node_id(self, node_id, attributes=None):
        '''Get topology for the model definition specified by node id.'''
        if attributes:
            self.params['attributes']=attributes
        response = dr.discoRequest(self, "/models/by_node_id/{}/topology".format(node_id))
        return response

    def get_nodecount_by_node_id(self, node_id):
        '''Get node count for the model definition specified by node id.'''
        response = dr.discoRequest(self, "/models/by_node_id/{}/nodecount".format(node_id))
        return response

    def get_nodes_by_node_id(self, node_id, format=None, limit=100, results_id=None, delete=False, kind=None):
        '''Get nodes for the model definition specified by node id.'''
        if format:
            self.params['format'] = format
        if results_id:
            self.params['results_id'] = results_id    
        self.params['limit'] = limit
        self.params['delete'] = delete
        if kind:
            response = dr.discoRequest(self, "/models/by_node_id/{}/nodes/{}".format(node_id,kind))
        else:
            response = dr.discoRequest(self, "/models/by_node_id/{}/nodes".format(node_id))
        return response
    