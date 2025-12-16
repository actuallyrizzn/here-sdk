"""
Unit tests for Traffic API v7 client
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import requests
from here_traffic_sdk.v7 import TrafficAPIv7
from here_traffic_sdk.models import LocationReference, GeospatialFilter


class TestTrafficAPIv7:
    """Test TrafficAPIv7 class"""
    
    def test_init(self, auth_client_api_key):
        """Test TrafficAPIv7 initialization"""
        client = TrafficAPIv7(auth_client_api_key)
        assert client.auth_client == auth_client_api_key
        assert client.BASE_URL == "https://data.traffic.hereapi.com/v7"
        assert client.session is not None
    
    def test_get_flow(self, auth_client_api_key, mock_flow_response, mock_requests_session):
        """Test get_flow method"""
        mock_response = Mock()
        mock_response.json.return_value = mock_flow_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response
        
        client = TrafficAPIv7(auth_client_api_key)
        result = client.get_flow(
            location_referencing=LocationReference.SHAPE,
            geospatial_filter="circle:51.50643,-0.12719;r=1000"
        )
        
        assert result.data == mock_flow_response
        mock_requests_session.get.assert_called_once()
        call_args = mock_requests_session.get.call_args
        assert "flow" in call_args[0][0]
        assert call_args[1]["params"]["locationReferencing"] == "shape"
        assert call_args[1]["params"]["in"] == "circle:51.50643,-0.12719;r=1000"
        assert call_args[1]["params"]["apiKey"] == "test_api_key_12345"
    
    def test_get_flow_with_oauth(self, auth_client_oauth, mock_flow_response, mock_oauth_token_response, mock_requests_session, mock_requests_post):
        """Test get_flow with OAuth authentication"""
        # Mock OAuth token response
        oauth_response = Mock()
        oauth_response.json.return_value = mock_oauth_token_response
        oauth_response.raise_for_status = Mock()
        mock_requests_post.return_value = oauth_response
        
        # Mock API response
        api_response = Mock()
        api_response.json.return_value = mock_flow_response
        api_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = api_response
        
        client = TrafficAPIv7(auth_client_oauth)
        result = client.get_flow(
            location_referencing=LocationReference.SHAPE,
            geospatial_filter="circle:51.50643,-0.12719;r=1000"
        )
        
        assert result.data == mock_flow_response
        assert "Authorization" in mock_requests_session.get.call_args[1]["headers"]
    
    def test_get_flow_with_additional_params(self, auth_client_api_key, mock_flow_response, mock_requests_session):
        """Test get_flow with additional parameters"""
        mock_response = Mock()
        mock_response.json.return_value = mock_flow_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response
        
        client = TrafficAPIv7(auth_client_api_key)
        client.get_flow(
            location_referencing=LocationReference.TMC,
            geospatial_filter="bbox:51.5,-0.13;51.51,-0.12",
            custom_param="value"
        )
        
        call_args = mock_requests_session.get.call_args
        assert call_args[1]["params"]["custom_param"] == "value"
    
    def test_get_flow_http_error(self, auth_client_api_key, mock_requests_session):
        """Test get_flow with HTTP error"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("400 Bad Request")
        mock_requests_session.get.return_value = mock_response
        
        client = TrafficAPIv7(auth_client_api_key)
        with pytest.raises(requests.HTTPError):
            client.get_flow(
                location_referencing=LocationReference.SHAPE,
                geospatial_filter="circle:51.50643,-0.12719;r=1000"
            )
    
    def test_get_flow_circle(self, auth_client_api_key, mock_flow_response, mock_requests_session):
        """Test get_flow_circle convenience method"""
        mock_response = Mock()
        mock_response.json.return_value = mock_flow_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response
        
        client = TrafficAPIv7(auth_client_api_key)
        result = client.get_flow_circle(51.50643, -0.12719, 1000)
        
        assert result.data == mock_flow_response
        call_args = mock_requests_session.get.call_args
        assert "circle:51.50643,-0.12719;r=1000" in call_args[1]["params"]["in"]
    
    def test_get_flow_circle_with_location_reference(self, auth_client_api_key, mock_flow_response, mock_requests_session):
        """Test get_flow_circle with custom location reference"""
        mock_response = Mock()
        mock_response.json.return_value = mock_flow_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response
        
        client = TrafficAPIv7(auth_client_api_key)
        client.get_flow_circle(51.50643, -0.12719, 1000, LocationReference.TMC)
        
        call_args = mock_requests_session.get.call_args
        assert call_args[1]["params"]["locationReferencing"] == "tmc"
    
    def test_get_flow_bbox(self, auth_client_api_key, mock_flow_response, mock_requests_session):
        """Test get_flow_bbox convenience method"""
        mock_response = Mock()
        mock_response.json.return_value = mock_flow_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response
        
        client = TrafficAPIv7(auth_client_api_key)
        result = client.get_flow_bbox(51.5, -0.13, 51.51, -0.12)
        
        assert result.data == mock_flow_response
        call_args = mock_requests_session.get.call_args
        assert "bbox:51.5,-0.13;51.51,-0.12" in call_args[1]["params"]["in"]
    
    def test_get_incidents(self, auth_client_api_key, mock_incidents_response, mock_requests_session):
        """Test get_incidents method"""
        mock_response = Mock()
        mock_response.json.return_value = mock_incidents_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response
        
        client = TrafficAPIv7(auth_client_api_key)
        result = client.get_incidents(
            location_referencing=LocationReference.SHAPE,
            geospatial_filter="circle:51.50643,-0.12719;r=1000"
        )
        
        assert result.data == mock_incidents_response
        mock_requests_session.get.assert_called_once()
        call_args = mock_requests_session.get.call_args
        assert "incidents" in call_args[0][0]
        assert call_args[1]["params"]["locationReferencing"] == "shape"
    
    def test_get_incidents_circle(self, auth_client_api_key, mock_incidents_response, mock_requests_session):
        """Test get_incidents_circle convenience method"""
        mock_response = Mock()
        mock_response.json.return_value = mock_incidents_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response
        
        client = TrafficAPIv7(auth_client_api_key)
        result = client.get_incidents_circle(51.50643, -0.12719, 1000)
        
        assert result.data == mock_incidents_response
        call_args = mock_requests_session.get.call_args
        assert "circle:51.50643,-0.12719;r=1000" in call_args[1]["params"]["in"]
    
    def test_get_incidents_bbox(self, auth_client_api_key, mock_incidents_response, mock_requests_session):
        """Test get_incidents_bbox convenience method"""
        mock_response = Mock()
        mock_response.json.return_value = mock_incidents_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response
        
        client = TrafficAPIv7(auth_client_api_key)
        result = client.get_incidents_bbox(51.5, -0.13, 51.51, -0.12)
        
        assert result.data == mock_incidents_response
        call_args = mock_requests_session.get.call_args
        assert "bbox:51.5,-0.13;51.51,-0.12" in call_args[1]["params"]["in"]
    
    def test_get_availability(self, auth_client_api_key, mock_availability_response, mock_requests_session):
        """Test get_availability method"""
        mock_response = Mock()
        mock_response.json.return_value = mock_availability_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response
        
        client = TrafficAPIv7(auth_client_api_key)
        result = client.get_availability()
        
        assert result.data == mock_availability_response
        mock_requests_session.get.assert_called_once()
        call_args = mock_requests_session.get.call_args
        assert "availability" in call_args[0][0]
    
    def test_get_availability_with_params(self, auth_client_api_key, mock_availability_response, mock_requests_session):
        """Test get_availability with additional parameters"""
        mock_response = Mock()
        mock_response.json.return_value = mock_availability_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response
        
        client = TrafficAPIv7(auth_client_api_key)
        client.get_availability(custom_param="value")
        
        call_args = mock_requests_session.get.call_args
        assert call_args[1]["params"]["custom_param"] == "value"
    
    def test_all_location_references(self, auth_client_api_key, mock_flow_response, mock_requests_session):
        """Test all location reference types work"""
        mock_response = Mock()
        mock_response.json.return_value = mock_flow_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response
        
        client = TrafficAPIv7(auth_client_api_key)
        
        for ref in [LocationReference.SHAPE, LocationReference.TMC, LocationReference.OLR]:
            client.get_flow(
                location_referencing=ref,
                geospatial_filter="circle:51.50643,-0.12719;r=1000"
            )
            call_args = mock_requests_session.get.call_args
            assert call_args[1]["params"]["locationReferencing"] == ref.value

