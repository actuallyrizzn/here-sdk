"""
Unit tests for Traffic API v6.3 client
"""

import pytest
from unittest.mock import Mock, patch
import requests
from here_traffic_sdk.v6 import TrafficAPIv6


class TestTrafficAPIv6:
    """Test TrafficAPIv6 class"""
    
    def test_init(self, auth_client_api_key):
        """Test TrafficAPIv6 initialization"""
        client = TrafficAPIv6(auth_client_api_key)
        assert client.auth_client == auth_client_api_key
        assert client.BASE_URL == "https://traffic.api.here.com/traffic/6.3"
        assert client.session is not None
    
    def test_get_flow(self, auth_client_api_key, mock_flow_response, mock_requests_session):
        """Test get_flow method"""
        mock_response = Mock()
        mock_response.json.return_value = mock_flow_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response
        
        client = TrafficAPIv6(auth_client_api_key)
        result = client.get_flow("51.5,-0.13;51.51,-0.12")
        
        assert result.data == mock_flow_response
        mock_requests_session.get.assert_called_once()
        call_args = mock_requests_session.get.call_args
        assert "flow.json" in call_args[0][0]
        assert call_args[1]["params"]["bbox"] == "51.5,-0.13;51.51,-0.12"
        assert call_args[1]["params"]["apiKey"] == "test_api_key_12345"
    
    def test_get_flow_with_additional_params(self, auth_client_api_key, mock_flow_response, mock_requests_session):
        """Test get_flow with additional parameters"""
        mock_response = Mock()
        mock_response.json.return_value = mock_flow_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response
        
        client = TrafficAPIv6(auth_client_api_key)
        client.get_flow("51.5,-0.13;51.51,-0.12", custom_param="value")
        
        call_args = mock_requests_session.get.call_args
        assert call_args[1]["params"]["custom_param"] == "value"
    
    def test_get_flow_http_error(self, auth_client_api_key, mock_requests_session):
        """Test get_flow with HTTP error"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("400 Bad Request")
        mock_requests_session.get.return_value = mock_response
        
        client = TrafficAPIv6(auth_client_api_key)
        with pytest.raises(requests.HTTPError):
            client.get_flow("51.5,-0.13;51.51,-0.12")
    
    def test_get_flow_bbox(self, auth_client_api_key, mock_flow_response, mock_requests_session):
        """Test get_flow_bbox convenience method"""
        mock_response = Mock()
        mock_response.json.return_value = mock_flow_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response
        
        client = TrafficAPIv6(auth_client_api_key)
        result = client.get_flow_bbox(51.5, -0.13, 51.51, -0.12)
        
        assert result.data == mock_flow_response
        call_args = mock_requests_session.get.call_args
        assert call_args[1]["params"]["bbox"] == "51.5,-0.13;51.51,-0.12"
    
    def test_get_incidents(self, auth_client_api_key, mock_incidents_response, mock_requests_session):
        """Test get_incidents method"""
        mock_response = Mock()
        mock_response.json.return_value = mock_incidents_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response
        
        client = TrafficAPIv6(auth_client_api_key)
        result = client.get_incidents("51.5,-0.13;51.51,-0.12")
        
        assert result.data == mock_incidents_response
        mock_requests_session.get.assert_called_once()
        call_args = mock_requests_session.get.call_args
        assert "incidents.json" in call_args[0][0]
        assert call_args[1]["params"]["bbox"] == "51.5,-0.13;51.51,-0.12"
    
    def test_get_incidents_bbox(self, auth_client_api_key, mock_incidents_response, mock_requests_session):
        """Test get_incidents_bbox convenience method"""
        mock_response = Mock()
        mock_response.json.return_value = mock_incidents_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response
        
        client = TrafficAPIv6(auth_client_api_key)
        result = client.get_incidents_bbox(51.5, -0.13, 51.51, -0.12)
        
        assert result.data == mock_incidents_response
        call_args = mock_requests_session.get.call_args
        assert call_args[1]["params"]["bbox"] == "51.5,-0.13;51.51,-0.12"
    
    def test_get_incidents_with_oauth(self, auth_client_oauth, mock_incidents_response, mock_oauth_token_response, mock_requests_session, mock_requests_post):
        """Test get_incidents with OAuth authentication"""
        # Mock OAuth token response
        oauth_response = Mock()
        oauth_response.json.return_value = mock_oauth_token_response
        oauth_response.raise_for_status = Mock()
        mock_requests_post.return_value = oauth_response
        
        # Mock API response
        api_response = Mock()
        api_response.json.return_value = mock_incidents_response
        api_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = api_response
        
        client = TrafficAPIv6(auth_client_oauth)
        result = client.get_incidents("51.5,-0.13;51.51,-0.12")
        
        assert result.data == mock_incidents_response
        assert "Authorization" in mock_requests_session.get.call_args[1]["headers"]

