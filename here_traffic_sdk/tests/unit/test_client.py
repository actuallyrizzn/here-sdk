"""
Unit tests for main client
"""

import pytest
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

