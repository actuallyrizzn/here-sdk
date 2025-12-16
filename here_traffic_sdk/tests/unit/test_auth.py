"""
Unit tests for authentication module
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import threading
import time
import requests
from here_traffic_sdk.auth import AuthClient, AuthMethod
from here_traffic_sdk.exceptions import HereAuthenticationError


class TestAuthClient:
    """Test AuthClient class"""
    
    def test_init_with_api_key(self, mock_api_key):
        """Test AuthClient initialization with API key"""
        client = AuthClient(api_key=mock_api_key, auth_method=AuthMethod.API_KEY)
        assert client.api_key == mock_api_key
        assert client.auth_method == AuthMethod.API_KEY
        assert client.access_key_id is None
        assert client.access_key_secret is None
    
    def test_init_with_oauth(self, mock_oauth_credentials):
        """Test AuthClient initialization with OAuth"""
        client = AuthClient(
            access_key_id=mock_oauth_credentials["access_key_id"],
            access_key_secret=mock_oauth_credentials["access_key_secret"],
            auth_method=AuthMethod.OAUTH
        )
        assert client.access_key_id == mock_oauth_credentials["access_key_id"]
        assert client.access_key_secret == mock_oauth_credentials["access_key_secret"]
        assert client.auth_method == AuthMethod.OAUTH
        assert client.api_key is None
    
    def test_get_auth_headers_api_key(self, auth_client_api_key):
        """Test getting auth headers with API key (should return empty)"""
        headers = auth_client_api_key.get_auth_headers()
        assert headers == {}
    
    def test_get_auth_headers_oauth(self, auth_client_oauth, mock_oauth_token_response, mock_requests_post):
        """Test getting auth headers with OAuth"""
        mock_response = Mock()
        mock_response.json.return_value = mock_oauth_token_response
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response
        
        headers = auth_client_oauth.get_auth_headers()
        assert "Authorization" in headers
        assert headers["Authorization"] == f"Bearer {mock_oauth_token_response['access_token']}"
    
    def test_get_auth_params_api_key(self, auth_client_api_key):
        """Test getting auth params with API key"""
        params = auth_client_api_key.get_auth_params()
        assert "apiKey" in params
        assert params["apiKey"] == "test_api_key_12345"
    
    def test_get_auth_params_oauth(self, auth_client_oauth):
        """Test getting auth params with OAuth (should return empty)"""
        params = auth_client_oauth.get_auth_params()
        assert params == {}
    
    def test_get_auth_params_missing_api_key(self):
        """Test getting auth params without API key raises error"""
        client = AuthClient(auth_method=AuthMethod.API_KEY)
        with pytest.raises(ValueError, match="API key is required"):
            client.get_auth_params()
    
    def test_get_oauth_token_first_time(self, auth_client_oauth, mock_oauth_token_response, mock_requests_post):
        """Test getting OAuth token for the first time"""
        mock_response = Mock()
        mock_response.json.return_value = mock_oauth_token_response
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response
        
        token = auth_client_oauth._get_oauth_token()
        assert token == mock_oauth_token_response["access_token"]
        assert auth_client_oauth._oauth_token == mock_oauth_token_response["access_token"]
        assert auth_client_oauth._token_expires_at is not None
        mock_requests_post.assert_called_once()
    
    def test_get_oauth_token_cached(self, auth_client_oauth, mock_oauth_token_response, mock_requests_post):
        """Test getting cached OAuth token"""
        mock_response = Mock()
        mock_response.json.return_value = mock_oauth_token_response
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response
        
        # First call
        token1 = auth_client_oauth._get_oauth_token()
        mock_requests_post.assert_called_once()
        
        # Second call should use cache
        token2 = auth_client_oauth._get_oauth_token()
        assert token1 == token2
        assert mock_requests_post.call_count == 1  # Still only called once
    
    def test_get_oauth_token_expired(self, auth_client_oauth, mock_oauth_token_response, mock_requests_post):
        """Test getting OAuth token when cached token is expired"""
        mock_response = Mock()
        mock_response.json.return_value = mock_oauth_token_response
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response
        
        # Set expired token
        auth_client_oauth._oauth_token = "old_token"
        auth_client_oauth._token_expires_at = datetime.now() - timedelta(hours=1)
        
        token = auth_client_oauth._get_oauth_token()
        assert token == mock_oauth_token_response["access_token"]
        assert mock_requests_post.call_count == 1
    
    def test_get_oauth_token_missing_credentials(self):
        """Test getting OAuth token without credentials raises error"""
        client = AuthClient(auth_method=AuthMethod.OAUTH)
        with pytest.raises(ValueError, match="OAuth credentials"):
            client._get_oauth_token()
    
    def test_get_oauth_token_http_error(self, auth_client_oauth, mock_requests_post):
        """Test OAuth token request with HTTP error"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.url = "https://account.api.here.com/oauth2/token"
        mock_requests_post.return_value = mock_response
        
        with pytest.raises(HereAuthenticationError):
            auth_client_oauth._get_oauth_token()
    
    def test_refresh_token(self, auth_client_oauth, mock_oauth_token_response, mock_requests_post):
        """Test manually refreshing OAuth token"""
        mock_response = Mock()
        mock_response.json.return_value = mock_oauth_token_response
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response
        
        # Set existing token
        auth_client_oauth._oauth_token = "old_token"
        auth_client_oauth._token_expires_at = datetime.now() + timedelta(hours=1)
        
        # Refresh
        auth_client_oauth.refresh_token()
        
        assert auth_client_oauth._oauth_token == mock_oauth_token_response["access_token"]
        mock_requests_post.assert_called_once()
    
    def test_oauth_token_refresh_before_expiry(self, auth_client_oauth, mock_oauth_token_response, mock_requests_post):
        """Test OAuth token is refreshed 5 minutes before expiry"""
        mock_response = Mock()
        mock_response.json.return_value = mock_oauth_token_response
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response
        
        # Set token expiring in 4 minutes (should refresh)
        auth_client_oauth._oauth_token = "old_token"
        auth_client_oauth._token_expires_at = datetime.now() + timedelta(minutes=4)
        
        token = auth_client_oauth._get_oauth_token()
        assert token == mock_oauth_token_response["access_token"]
        assert mock_requests_post.call_count == 1
    
    def test_oauth_token_not_refreshed_if_valid(self, auth_client_oauth, mock_oauth_token_response, mock_requests_post):
        """Test OAuth token is not refreshed if still valid"""
        mock_response = Mock()
        mock_response.json.return_value = mock_oauth_token_response
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response
        
        # Set token expiring in 10 minutes (should not refresh)
        auth_client_oauth._oauth_token = "valid_token"
        auth_client_oauth._token_expires_at = datetime.now() + timedelta(minutes=10)
        
        token = auth_client_oauth._get_oauth_token()
        assert token == "valid_token"
        assert mock_requests_post.call_count == 0
    
    def test_oauth_token_request_params(self, auth_client_oauth, mock_oauth_token_response, mock_requests_post):
        """Test OAuth token request includes correct parameters"""
        mock_response = Mock()
        mock_response.json.return_value = mock_oauth_token_response
        mock_response.status_code = 200
        mock_requests_post.return_value = mock_response
        
        auth_client_oauth._get_oauth_token()
        
        mock_requests_post.assert_called_once()
        call_args = mock_requests_post.call_args
        assert call_args[0][0] == AuthClient.OAUTH_TOKEN_URL
        assert call_args[1]["data"]["grant_type"] == "client_credentials"
        assert call_args[1]["data"]["client_id"] == auth_client_oauth.access_key_id
        assert call_args[1]["data"]["client_secret"] == auth_client_oauth.access_key_secret
        assert call_args[1]["headers"]["Content-Type"] == "application/x-www-form-urlencoded"

    def test_get_oauth_token_thread_safe_single_request(self, auth_client_oauth, mock_oauth_token_response, mock_requests_post):
        """Test concurrent callers only trigger one token request"""

        def slow_post(*args, **kwargs):
            # Force enough overlap that races would show up as multiple calls.
            time.sleep(0.05)
            resp = Mock()
            resp.status_code = 200
            resp.json.return_value = mock_oauth_token_response
            return resp

        mock_requests_post.side_effect = slow_post

        barrier = threading.Barrier(10)
        results = []
        errors = []

        def worker():
            try:
                barrier.wait()
                results.append(auth_client_oauth.get_auth_headers()["Authorization"])
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=5)

        assert not errors
        assert len(results) == 10
        assert all(r == f"Bearer {mock_oauth_token_response['access_token']}" for r in results)
        assert mock_requests_post.call_count == 1

