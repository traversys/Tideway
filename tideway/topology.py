# -*- coding: utf-8 -*-

import tideway

appliance = tideway.main.Appliance

class Topology(appliance):
    '''Retrieve topology data from the datastore.'''

    def get_data_nodes_graph(self, node_id, focus="software-connected", apply_rules=True, complete=False):
        '''Alternate API call for /data/nodes/node_id/graph'''
        self.params['focus'] = focus
        self.params['apply_rules'] = apply_rules
        self.params['complete'] = complete
        response = self.get("/data/nodes/{}/graph".format(node_id))
        return response

    def post_topology_nodes(self, body):
        '''Alternate API call for POST /topology/nodes.'''
        response = self.post("/topology/nodes", body)
        return response

    def post_topology_nodes_kinds(self, body):
        '''Alternate API call for POST /topology/nodes/kinds.'''
        response = self.post("/topology/nodes/kinds", body)
        return response

    def get_topology_viz_state(self):
        '''Get the current visualization state for the authenticated user.'''
        return self.get("/topology/visualization_state")

    def patch_topology_viz_state(self, body):
        '''Alternate API call for PATCH /topology/visualization_state'''
        response = self.patch("/topology/visualization_state", body)
        return response

    def put_topology_viz_state(self, body):
        '''Alternate API call for PUT /topology/visualization_state'''
        response = self.put("/topology/visualization_state", body)
        return response
