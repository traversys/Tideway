import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tideway


def test_data_get_data_nodes_graph_sends_complete():
    data = tideway.data('host', 'token')
    with patch('tideway.discoRequests.requests.get') as mock_get:
        mock_get.return_value = None
        data.get_data_nodes_graph('node', complete=True)
        params = mock_get.call_args.kwargs['params']
        assert params['complete'] is True


def test_topology_get_data_nodes_graph_sends_complete():
    topo = tideway.topology('host', 'token')
    with patch('tideway.discoRequests.requests.get') as mock_get:
        mock_get.return_value = None
        topo.get_data_nodes_graph('node', complete=True)
        params = mock_get.call_args.kwargs['params']
        assert params['complete'] is True
