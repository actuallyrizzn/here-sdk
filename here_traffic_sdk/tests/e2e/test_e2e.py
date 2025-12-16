"""
End-to-end tests for HERE Traffic SDK

These tests verify the complete flow from client initialization to API response.
Uses a mock HTTP server to simulate real API responses.
"""

import pytest
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from here_traffic_sdk import HereTrafficClient, LocationReference, GeospatialFilter, AuthMethod


class MockAPIHandler(BaseHTTPRequestHandler):
    """Mock HTTP server handler for HERE API"""
    
    def do_GET(self):
        """Handle GET requests"""
        if "/v7/flow" in self.path:
            response = {
                "flows": [
                    {
                        "freeFlowSpeed": 60.0,
                        "expectedSpeed": 45.0,
                        "jamFactor": 0.25
                    }
                ]
            }
        elif "/v7/incidents" in self.path:
            response = {
                "incidents": [
                    {
                        "type": "accident",
                        "criticality": "critical",
                        "description": "Test incident"
                    }
                ]
            }
        elif "/v7/availability" in self.path:
            response = {
                "available": True,
                "coverage": [{"country": "GB"}]
            }
        elif "/traffic/6.3/flow.json" in self.path:
            response = {
                "RWS": [{
                    "RW": [{
                        "FIS": [{
                            "FI": [{
                                "TMC": {"PC": 12345, "DE": "Test"}
                            }]
                        }]
                    }]
                }]
            }
        elif "/traffic/6.3/incidents.json" in self.path:
            response = {
                "TRAFFICITEMS": {
                    "TRAFFICITEM": [{
                        "TRAFFICITEMDESC": {
                            "TYPE": "accident"
                        }
                    }]
                }
            }
        elif "/v3/flow" in self.path:
            response = {
                "RWS": [{
                    "RW": [{
                        "FIS": [{
                            "FI": [{}]
                        }]
                    }]
                }]
            }
        else:
            response = {"error": "Unknown endpoint"}
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            return
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        """Handle POST requests (OAuth token)"""
        if "/oauth2/token" in self.path:
            response = {
                "access_token": "mock_access_token_12345",
                "token_type": "Bearer",
                "expires_in": 3600
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress log messages"""
        pass


@pytest.fixture(scope="module")
def mock_server():
    """Start mock HTTP server"""
    server = HTTPServer(("localhost", 8888), MockAPIHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield server
    server.shutdown()


@pytest.fixture
def e2e_client_api_key(mock_server):
    """Client configured to use mock server with API key"""
    with patch("here_traffic_sdk.v7.TrafficAPIv7.BASE_URL", "http://localhost:8888/v7"), \
         patch("here_traffic_sdk.v6.TrafficAPIv6.BASE_URL", "http://localhost:8888/traffic/6.3"), \
         patch("here_traffic_sdk.v3.TrafficAPIv3.BASE_URL", "http://localhost:8888/v3"), \
         patch("here_traffic_sdk.auth.AuthClient.OAUTH_TOKEN_URL", "http://localhost:8888/oauth2/token"):
        client = HereTrafficClient(api_key="test_key")
        yield client


@pytest.fixture
def e2e_client_oauth(mock_server):
    """Client configured to use mock server with OAuth"""
    with patch("here_traffic_sdk.v7.TrafficAPIv7.BASE_URL", "http://localhost:8888/v7"), \
         patch("here_traffic_sdk.v6.TrafficAPIv6.BASE_URL", "http://localhost:8888/traffic/6.3"), \
         patch("here_traffic_sdk.v3.TrafficAPIv3.BASE_URL", "http://localhost:8888/v3"), \
         patch("here_traffic_sdk.auth.AuthClient.OAUTH_TOKEN_URL", "http://localhost:8888/oauth2/token"):
        client = HereTrafficClient(
            access_key_id="test_id",
            access_key_secret="test_secret",
            auth_method=AuthMethod.OAUTH
        )
        yield client


class TestE2E:
    """End-to-end tests"""
    
    @pytest.mark.e2e
    def test_e2e_v7_flow_api_key(self, e2e_client_api_key):
        """E2E test: v7 flow endpoint with API key"""
        response = e2e_client_api_key.v7.get_flow_circle(51.50643, -0.12719, 1000)
        assert response.flows is not None
        assert len(response.flows) > 0
        assert response.free_flow_speeds[0] == 60.0
    
    @pytest.mark.e2e
    def test_e2e_v7_flow_oauth(self, e2e_client_oauth):
        """E2E test: v7 flow endpoint with OAuth"""
        response = e2e_client_oauth.v7.get_flow_circle(51.50643, -0.12719, 1000)
        assert response.flows is not None
        assert len(response.flows) > 0
    
    @pytest.mark.e2e
    def test_e2e_v7_incidents_api_key(self, e2e_client_api_key):
        """E2E test: v7 incidents endpoint with API key"""
        response = e2e_client_api_key.v7.get_incidents_circle(51.50643, -0.12719, 1000)
        assert response.incidents is not None
        assert len(response.incidents) > 0
        assert response.incident_count > 0
    
    @pytest.mark.e2e
    def test_e2e_v7_availability_api_key(self, e2e_client_api_key):
        """E2E test: v7 availability endpoint with API key"""
        response = e2e_client_api_key.v7.get_availability()
        assert response.available is True
        assert len(response.coverage_areas) > 0
    
    @pytest.mark.e2e
    def test_e2e_v6_flow_api_key(self, e2e_client_api_key):
        """E2E test: v6.3 flow endpoint with API key"""
        response = e2e_client_api_key.v6.get_flow_bbox(51.5, -0.13, 51.51, -0.12)
        assert response.data is not None
    
    @pytest.mark.e2e
    def test_e2e_v6_incidents_api_key(self, e2e_client_api_key):
        """E2E test: v6.3 incidents endpoint with API key"""
        response = e2e_client_api_key.v6.get_incidents_bbox(51.5, -0.13, 51.51, -0.12)
        assert response.data is not None
    
    @pytest.mark.e2e
    def test_e2e_v3_flow_api_key(self, e2e_client_api_key):
        """E2E test: v3 flow endpoint with API key"""
        response = e2e_client_api_key.v3.get_flow()
        assert response.data is not None
    
    @pytest.mark.e2e
    def test_e2e_complete_workflow(self, e2e_client_api_key):
        """E2E test: Complete workflow using multiple endpoints"""
        # Get flow data
        flow = e2e_client_api_key.v7.get_flow_circle(51.50643, -0.12719, 1000)
        assert flow.flows is not None
        
        # Get incidents
        incidents = e2e_client_api_key.v7.get_incidents_circle(51.50643, -0.12719, 1000)
        assert incidents.incidents is not None
        
        # Check availability
        availability = e2e_client_api_key.v7.get_availability()
        assert availability.available is True
    
    @pytest.mark.e2e
    def test_e2e_oauth_token_flow(self, e2e_client_oauth):
        """E2E test: OAuth token acquisition and usage"""
        # First call should acquire token
        response1 = e2e_client_oauth.v7.get_flow_circle(51.50643, -0.12719, 1000)
        assert response1.flows is not None
        
        # Second call should use cached token
        response2 = e2e_client_oauth.v7.get_flow_circle(51.50643, -0.12719, 1000)
        assert response2.flows is not None
    
    @pytest.mark.e2e
    def test_e2e_all_location_references(self, e2e_client_api_key):
        """E2E test: All location reference types"""
        for ref in [LocationReference.SHAPE, LocationReference.TMC, LocationReference.OLR]:
            response = e2e_client_api_key.v7.get_flow(
                location_referencing=ref,
                geospatial_filter=GeospatialFilter.circle(51.50643, -0.12719, 1000)
            )
            assert response.flows is not None
    
    @pytest.mark.e2e
    def test_e2e_geospatial_filters(self, e2e_client_api_key):
        """E2E test: All geospatial filter types"""
        # Circle filter
        circle_response = e2e_client_api_key.v7.get_flow_circle(51.50643, -0.12719, 1000)
        assert circle_response.flows is not None
        
        # Bbox filter
        bbox_response = e2e_client_api_key.v7.get_flow_bbox(51.5, -0.13, 51.51, -0.12)
        assert bbox_response.flows is not None
    
    @pytest.mark.e2e
    def test_e2e_response_model_methods(self, e2e_client_api_key):
        """E2E test: Response model helper methods"""
        incidents = e2e_client_api_key.v7.get_incidents_circle(51.50643, -0.12719, 1000)
        
        # Test helper methods
        assert incidents.incident_count > 0
        critical = incidents.get_critical_incidents()
        assert len(critical) > 0
        
        flow = e2e_client_api_key.v7.get_flow_circle(51.50643, -0.12719, 1000)
        assert len(flow.free_flow_speeds) > 0
        assert len(flow.expected_speeds) > 0
    
    @pytest.mark.e2e
    def test_e2e_client_properties(self, e2e_client_api_key):
        """E2E test: Client convenience properties"""
        # Test flow property
        flow = e2e_client_api_key.flow.get_flow_circle(51.50643, -0.12719, 1000)
        assert flow.flows is not None
        
        # Test incidents property
        incidents = e2e_client_api_key.incidents.get_incidents_circle(51.50643, -0.12719, 1000)
        assert incidents.incidents is not None
        
        # Test availability property
        availability = e2e_client_api_key.availability.get_availability()
        assert availability.available is True
    
    @pytest.mark.e2e
    def test_e2e_multiple_versions(self, e2e_client_api_key):
        """E2E test: Using multiple API versions"""
        # v7
        v7_flow = e2e_client_api_key.v7.get_flow_circle(51.50643, -0.12719, 1000)
        assert v7_flow.flows is not None
        
        # v6.3
        v6_flow = e2e_client_api_key.v6.get_flow_bbox(51.5, -0.13, 51.51, -0.12)
        assert v6_flow.data is not None
        
        # v3
        v3_flow = e2e_client_api_key.v3.get_flow()
        assert v3_flow.data is not None

