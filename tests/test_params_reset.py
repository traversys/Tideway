import tideway
from unittest.mock import patch, MagicMock, ANY


def test_params_cleared_after_search():
    tw = tideway.appliance('host', 'token')
    with patch('tideway.discoRequests.requests.post') as mock_post:
        mock_post.return_value = MagicMock(status_code=200, ok=True)
        tw.data().search({'query': 'search'}, offset=1)
        assert tw.params == {'limit': 100, 'delete': False}


def test_params_not_leak_between_calls():
    tw = tideway.appliance('host', 'token')
    with patch('tideway.discoRequests.requests.post') as mock_post, \
         patch('tideway.discoRequests.requests.get') as mock_get:
        mock_post.return_value = MagicMock(status_code=200, ok=True)
        mock_get.return_value = MagicMock(status_code=200, ok=True)
        tw.data().search({'query': 'search'}, offset=2)
        tw.get('/about')
        assert mock_get.call_args[1]['params'] == {'limit': 100, 'delete': False}
        assert tw.params == {'limit': 100, 'delete': False}


def test_params_reset_after_get_data_kinds_values():
    tw = tideway.appliance('host', 'token')
    with patch('tideway.discoRequests.requests.get') as mock_get:
        mock_get.return_value = MagicMock(status_code=200, ok=True)
        tw.data().get_data_kinds_values('Host', 'name', offset=5)
        assert mock_get.call_args[1]['params']['offset'] == 5
        assert tw.params == {'limit': 100, 'delete': False}

