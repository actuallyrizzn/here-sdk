"""
Unit tests for main client
"""

import pytest
from unittest.mock import Mock
from here_traffic_sdk.client import HereTrafficClient
from here_traffic_sdk.auth import AuthMethod
from here_traffic_sdk.config import HereTrafficConfig
from here_traffic_sdk.models import LocationReference


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

    def test_config_overrides_base_url(self, mock_api_key, mock_flow_response, mock_requests_session):
        """Test passing config changes the endpoint URL used"""
        cfg = HereTrafficConfig(v7_base_url="https://example.test/v7")
        client = HereTrafficClient(api_key=mock_api_key, config=cfg)

        mock_response = Mock()
        mock_response.json.return_value = mock_flow_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response

        client.v7.get_flow(LocationReference.SHAPE, "circle:51.50643,-0.12719;r=1000")

        called_url = mock_requests_session.get.call_args[0][0]
        assert called_url.startswith("https://example.test/v7/")

