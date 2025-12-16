"""
Integration tests for HERE Traffic SDK

These tests verify that components work together correctly.
Uses mocked HTTP responses to test the full request/response cycle.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import requests
from here_traffic_sdk import HereTrafficClient, LocationReference, GeospatialFilter, AuthMethod
from here_traffic_sdk.auth import AuthClient


class TestIntegration:
    """Integration tests for SDK components"""
    
    def test_full_flow_api_key_auth(self, mock_api_key, mock_flow_response, mock_requests_session):
        """Test complete flow with API key authentication"""
        mock_response = Mock()
        mock_response.json.return_value = mock_flow_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response
        
        client = HereTrafficClient(api_key=mock_api_key)
        response = client.v7.get_flow_circle(51.50643, -0.12719, 1000)
        
        assert response.flows is not None
        assert len(response.flows) == 2
        assert response.free_flow_speeds == [60.0, 50.0]
        
        # Verify request was made correctly
        call_args = mock_requests_session.get.call_args
        assert "flow" in call_args[0][0]
        assert call_args[1]["params"]["apiKey"] == mock_api_key
    
    def test_full_flow_oauth_auth(self, mock_oauth_credentials, mock_flow_response, mock_oauth_token_response, mock_requests_session, mock_requests_post):
        """Test complete flow with OAuth authentication"""
        # Mock OAuth token
        oauth_response = Mock()
        oauth_response.json.return_value = mock_oauth_token_response
        oauth_response.raise_for_status = Mock()
        mock_requests_post.return_value = oauth_response
        
        # Mock API response
        api_response = Mock()
        api_response.json.return_value = mock_flow_response
        api_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = api_response
        
        client = HereTrafficClient(
            access_key_id=mock_oauth_credentials["access_key_id"],
            access_key_secret=mock_oauth_credentials["access_key_secret"],
            auth_method=AuthMethod.OAUTH
        )
        response = client.v7.get_flow_circle(51.50643, -0.12719, 1000)
        
        assert response.flows is not None
        assert len(response.flows) == 2
        
        # Verify OAuth token was requested
        mock_requests_post.assert_called_once()
        # Verify API request had auth header
        assert "Authorization" in mock_requests_session.get.call_args[1]["headers"]
    
    def test_incidents_with_filtering(self, mock_api_key, mock_incidents_response, mock_requests_session):
        """Test incidents endpoint with response filtering"""
        mock_response = Mock()
        mock_response.json.return_value = mock_incidents_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response
        
        client = HereTrafficClient(api_key=mock_api_key)
        response = client.v7.get_incidents_circle(51.50643, -0.12719, 1000)
        
        # Test response model methods
        assert response.incident_count == 2
        critical = response.get_critical_incidents()
        assert len(critical) == 1
        assert critical[0]["criticality"] == "critical"
        
        accidents = response.get_incidents_by_type("accident")
        assert len(accidents) == 1
    
    def test_multiple_api_versions(self, mock_api_key, mock_flow_response, mock_incidents_response, mock_requests_session):
        """Test using multiple API versions in same client"""
        mock_flow_resp = Mock()
        mock_flow_resp.json.return_value = mock_flow_response
        mock_flow_resp.raise_for_status = Mock()
        
        mock_inc_resp = Mock()
        mock_inc_resp.json.return_value = mock_incidents_response
        mock_inc_resp.raise_for_status = Mock()
        
        mock_requests_session.get.side_effect = [mock_flow_resp, mock_inc_resp]
        
        client = HereTrafficClient(api_key=mock_api_key)
        
        # Use v7
        flow_v7 = client.v7.get_flow_circle(51.50643, -0.12719, 1000)
        assert flow_v7.flows is not None
        
        # Use v6.3
        flow_v6 = client.v6.get_flow_bbox(51.5, -0.13, 51.51, -0.12)
        assert flow_v6.flows is not None
    
    def test_geospatial_filter_helpers(self, mock_api_key, mock_flow_response, mock_requests_session):
        """Test geospatial filter helpers work with API calls"""
        mock_response = Mock()
        mock_response.json.return_value = mock_flow_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response
        
        client = HereTrafficClient(api_key=mock_api_key)
        
        # Test circle filter
        circle_filter = GeospatialFilter.circle(51.50643, -0.12719, 1000)
        response1 = client.v7.get_flow(LocationReference.SHAPE, circle_filter)
        assert response1.flows is not None
        
        # Test bbox filter
        bbox_filter = GeospatialFilter.bbox(51.5, -0.13, 51.51, -0.12)
        response2 = client.v7.get_flow(LocationReference.SHAPE, bbox_filter)
        assert response2.flows is not None
    
    def test_error_handling_flow(self, mock_api_key, mock_requests_session):
        """Test error handling in request flow"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("401 Unauthorized")
        mock_requests_session.get.return_value = mock_response
        
        client = HereTrafficClient(api_key=mock_api_key)
        
        with pytest.raises(requests.HTTPError):
            client.v7.get_flow_circle(51.50643, -0.12719, 1000)
    
    def test_oauth_token_refresh_flow(self, mock_oauth_credentials, mock_flow_response, mock_oauth_token_response, mock_requests_session, mock_requests_post):
        """Test OAuth token refresh during API call"""
        # First token response
        token1 = mock_oauth_token_response.copy()
        token1["access_token"] = "token1"
        
        # Second token response (after refresh)
        token2 = mock_oauth_token_response.copy()
        token2["access_token"] = "token2"
        
        oauth_resp1 = Mock()
        oauth_resp1.json.return_value = token1
        oauth_resp1.raise_for_status = Mock()
        
        oauth_resp2 = Mock()
        oauth_resp2.json.return_value = token2
        oauth_resp2.raise_for_status = Mock()
        
        api_response = Mock()
        api_response.json.return_value = mock_flow_response
        api_response.raise_for_status = Mock()
        
        mock_requests_post.side_effect = [oauth_resp1, oauth_resp2]
        mock_requests_session.get.return_value = api_response
        
        client = HereTrafficClient(
            access_key_id=mock_oauth_credentials["access_key_id"],
            access_key_secret=mock_oauth_credentials["access_key_secret"],
            auth_method=AuthMethod.OAUTH
        )
        
        # Make first call
        response1 = client.v7.get_flow_circle(51.50643, -0.12719, 1000)
        assert response1.flows is not None
        
        # Force token expiry and make second call
        client.auth_client._token_expires_at = None
        response2 = client.v7.get_flow_circle(51.50643, -0.12719, 1000)
        assert response2.flows is not None
        
        # Should have requested token twice
        assert mock_requests_post.call_count == 2
    
    def test_all_location_references(self, mock_api_key, mock_flow_response, mock_requests_session):
        """Test all location reference types work end-to-end"""
        mock_response = Mock()
        mock_response.json.return_value = mock_flow_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response
        
        client = HereTrafficClient(api_key=mock_api_key)
        
        for ref in [LocationReference.SHAPE, LocationReference.TMC, LocationReference.OLR]:
            response = client.v7.get_flow(
                location_referencing=ref,
                geospatial_filter=GeospatialFilter.circle(51.50643, -0.12719, 1000)
            )
            assert response.flows is not None
    
    def test_availability_integration(self, mock_api_key, mock_availability_response, mock_requests_session):
        """Test availability endpoint integration"""
        mock_response = Mock()
        mock_response.json.return_value = mock_availability_response
        mock_response.raise_for_status = Mock()
        mock_requests_session.get.return_value = mock_response
        
        client = HereTrafficClient(api_key=mock_api_key)
        response = client.v7.get_availability()
        
        assert response.available is True
        assert len(response.coverage_areas) == 1
        assert response.coverage_areas[0]["country"] == "GB"
    
    def test_client_properties(self, mock_api_key, mock_flow_response, mock_incidents_response, mock_availability_response, mock_requests_session):
        """Test client convenience properties"""
        mock_flow_resp = Mock()
        mock_flow_resp.json.return_value = mock_flow_response
        mock_flow_resp.raise_for_status = Mock()
        
        mock_inc_resp = Mock()
        mock_inc_resp.json.return_value = mock_incidents_response
        mock_inc_resp.raise_for_status = Mock()
        
        mock_avail_resp = Mock()
        mock_avail_resp.json.return_value = mock_availability_response
        mock_avail_resp.raise_for_status = Mock()
        
        mock_requests_session.get.side_effect = [mock_flow_resp, mock_inc_resp, mock_avail_resp]
        
        client = HereTrafficClient(api_key=mock_api_key)
        
        # Test flow property
        flow_response = client.flow.get_flow_circle(51.50643, -0.12719, 1000)
        assert flow_response.flows is not None
        
        # Test incidents property
        incidents_response = client.incidents.get_incidents_circle(51.50643, -0.12719, 1000)
        assert incidents_response.incidents is not None
        
        # Test availability property
        availability_response = client.availability.get_availability()
        assert availability_response.available is True

