"""
Unit tests for main client
"""

import pytest
from unittest.mock import Mock
from here_traffic_sdk.client import HereTrafficClient
from here_traffic_sdk.auth import AuthMethod


class TestHereTrafficClient:
    """Test HereTrafficClient class"""
    
    def test_init_with_api_key(self, mock_api_key):
        """Test HereTrafficClient initialization with API key"""
        client = HereTrafficClient(api_key=mock_api_key)
        assert client.auth_client.api_key == mock_api_key
        assert client.auth_client.auth_method == AuthMethod.API_KEY
        assert client.v7 is not None
        assert client.v6 is not None
        assert client.v3 is not None
    
    def test_init_with_oauth(self, mock_oauth_credentials):
        """Test HereTrafficClient initialization with OAuth"""
        client = HereTrafficClient(
            access_key_id=mock_oauth_credentials["access_key_id"],
            access_key_secret=mock_oauth_credentials["access_key_secret"],
            auth_method=AuthMethod.OAUTH
        )
        assert client.auth_client.access_key_id == mock_oauth_credentials["access_key_id"]
        assert client.auth_client.auth_method == AuthMethod.OAUTH
        assert client.v7 is not None
        assert client.v6 is not None
        assert client.v3 is not None
    
    def test_flow_property(self, mock_api_key):
        """Test flow property returns v7 client"""
        client = HereTrafficClient(api_key=mock_api_key)
        assert client.flow == client.v7
    
    def test_incidents_property(self, mock_api_key):
        """Test incidents property returns v7 client"""
        client = HereTrafficClient(api_key=mock_api_key)
        assert client.incidents == client.v7
    
    def test_availability_property(self, mock_api_key):
        """Test availability property returns v7 client"""
        client = HereTrafficClient(api_key=mock_api_key)
        assert client.availability == client.v7
    
    def test_all_clients_share_auth(self, mock_api_key):
        """Test all API clients share the same auth client"""
        client = HereTrafficClient(api_key=mock_api_key)
        assert client.v7.auth_client == client.auth_client
        assert client.v6.auth_client == client.auth_client
        assert client.v3.auth_client == client.auth_client

    def test_close_closes_shared_session(self, mock_api_key, mock_requests_session):
        """Test close() closes shared session"""
        client = HereTrafficClient(api_key=mock_api_key)
        client.close()
        mock_requests_session.close.assert_called_once()

    def test_context_manager_closes_shared_session(self, mock_api_key, mock_requests_session):
        """Test context manager closes shared session on exit"""
        mock_requests_session.close.reset_mock()
        with HereTrafficClient(api_key=mock_api_key) as client:
            assert client.v7 is not None
        mock_requests_session.close.assert_called_once()

    def test_http_config_propagates_timeout_and_verify(self, mock_api_key, mock_availability_response, mock_requests_session):
        """Test HereTrafficClient timeout/verify are forwarded to requests"""
        mock_response = Mock()
        mock_response.json.return_value = mock_availability_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response

        client = HereTrafficClient(api_key=mock_api_key, timeout=1.5, verify_ssl=False, request_id_factory=lambda: "rid")
        client.v7.get_availability()

        call_args = mock_requests_session.get.call_args
        assert call_args[1]["timeout"] == 1.5
        assert call_args[1]["verify"] is False

