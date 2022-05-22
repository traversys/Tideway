# -*- coding: utf-8 -*-

import tideway

dr = tideway.discoRequests
appliance = tideway.main.Appliance

class Topology(appliance):
    '''Retrieve topology data from the datastore.'''

    def get_data_nodes_graph(self, node_id, focus="sofware-connected", apply_rules=True, complete=False):
        '''Alternate API call for /data/nodes/node_id/graph'''
        self.params['focus'] = focus
        self.params['apply_rules'] = apply_rules
        self.params['complete'] = complete
        response = dr.discoRequest(self, "/data/nodes/{}/graph".format(node_id))
        return response

    def graphNode(self, node_id, focus="sofware-connected", apply_rules=True):
        '''
            Graph data represents a set of nodes and relationships that are
            associated to the given node.
        '''
        self.params['focus'] = focus
        self.params['apply_rules'] = apply_rules
        response = dr.discoRequest(self, "/data/nodes/{}/graph".format(node_id))
        return response

    def post_topology_nodes(self, body):
        '''Alternate API call for POST /topology/nodes.'''
        response = dr.discoPost(self, "/topology/nodes", body)
        return response

    def getNodes(self, body):
        '''Get topology data from one or more starting nodes.'''
        response = dr.discoPost(self, "/topology/nodes", body)
        return response

    def post_topology_nodes_kinds(self, body):
        '''Alternate API call for POST /topology/nodes/kinds.'''
        response = dr.discoPost(self, "/topology/nodes/kinds", body)
        return response

    def getNodeKinds(self, body):
        '''
            Get nodes of the specified kinds which are related to a given set of
            nodes.
        '''
        response = dr.discoPost(self, "/topology/nodes/kinds", body)
        return response

    def visualizationState(self):
        '''
            Get the current state of the visualization for the authenticated
            user.
        '''
        response = dr.discoRequest(self, "/topology/visualization_state")
        return response
    get_topology_viz_state = property(visualizationState)

    def patch_topology_viz_state(self, body):
        '''Alternate API call for PATCH /topology/visualization_state'''
        response = dr.discoPatch(self, "/topology/visualization_state", body)
        return response

    def updateVizState(self, body):
        '''
            Update one or more attributes of the current state of the
            visualization for the authenticated user.
        '''
        response = dr.discoPatch(self, "/topology/visualization_state", body)
        return response

    def put_topology_viz_state(self, body):
        '''Alternate API call for PUT /topology/visualization_state'''
        response = dr.discoPut(self, "/topology/visualization_state", body)
        return response

    def replaceVizState(self, body):
        '''
            Update any or all of the attributes of the current state of the
            visualization for the authenticated user.
        '''
        response = dr.discoPut(self, "/topology/visualization_state", body)
        return response
