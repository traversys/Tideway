import tideway
from unittest.mock import patch


def test_get_knowledge_trigger_patterns_sends_lookup_param():
    k = tideway.knowledge('host', 'token')
    with patch('tideway.discoRequests.requests.get') as mock_get:
        mock_get.return_value = None
        k.getKnowledgeTriggerPatterns(lookup_data_sources=True)
        params = mock_get.call_args.kwargs['params']
        assert params['lookup_data_sources'] is True

