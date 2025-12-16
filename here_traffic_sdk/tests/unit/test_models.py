"""
Unit tests for models module
"""

import pytest
from here_traffic_sdk.models import (
    LocationReference,
    GeospatialFilter,
    TrafficFlowResponse,
    TrafficIncidentResponse,
    AvailabilityResponse,
)


class TestLocationReference:
    """Test LocationReference enum"""
    
    def test_location_reference_values(self):
        """Test LocationReference enum values"""
        assert LocationReference.SHAPE.value == "shape"
        assert LocationReference.TMC.value == "tmc"
        assert LocationReference.OLR.value == "olr"


class TestGeospatialFilter:
    """Test GeospatialFilter utility class"""
    
    def test_circle_filter(self):
        """Test creating circle filter"""
        filter_str = GeospatialFilter.circle(51.50643, -0.12719, 1000)
        assert filter_str == "circle:51.50643,-0.12719;r=1000"
    
    def test_circle_filter_different_values(self):
        """Test circle filter with different values"""
        filter_str = GeospatialFilter.circle(40.7128, -74.0060, 500)
        assert filter_str == "circle:40.7128,-74.0060;r=500"
    
    def test_bbox_filter(self):
        """Test creating bounding box filter"""
        filter_str = GeospatialFilter.bbox(51.5, -0.13, 51.51, -0.12)
        assert filter_str == "bbox:51.5,-0.13;51.51,-0.12"
    
    def test_bbox_filter_different_values(self):
        """Test bbox filter with different values"""
        filter_str = GeospatialFilter.bbox(40.7, -74.0, 40.8, -73.9)
        assert filter_str == "bbox:40.7,-74.0;40.8,-73.9"
    
    def test_corridor_filter(self):
        """Test creating corridor filter"""
        encoded_polyline = "encoded_polyline_string_123"
        filter_str = GeospatialFilter.corridor(encoded_polyline)
        assert filter_str == f"corridor:{encoded_polyline}"


class TestTrafficFlowResponse:
    """Test TrafficFlowResponse model"""
    
    def test_init_with_data(self, mock_flow_response):
        """Test TrafficFlowResponse initialization"""
        response = TrafficFlowResponse(data=mock_flow_response)
        assert response.data == mock_flow_response
        assert response.raw_response == mock_flow_response
    
    def test_init_with_raw_response(self, mock_flow_response):
        """Test TrafficFlowResponse with custom raw_response"""
        raw = {"custom": "data"}
        response = TrafficFlowResponse(data=mock_flow_response, raw_response=raw)
        assert response.data == mock_flow_response
        assert response.raw_response == raw
    
    def test_flows_property(self, mock_flow_response):
        """Test flows property"""
        response = TrafficFlowResponse(data=mock_flow_response)
        flows = response.flows
        assert len(flows) == 2
        assert flows[0]["freeFlowSpeed"] == 60.0
    
    def test_flows_property_empty(self):
        """Test flows property with empty data"""
        response = TrafficFlowResponse(data={})
        assert response.flows == []
    
    def test_flows_property_missing_key(self):
        """Test flows property when key is missing"""
        response = TrafficFlowResponse(data={"other": "data"})
        assert response.flows == []
    
    def test_free_flow_speeds_property(self, mock_flow_response):
        """Test free_flow_speeds property"""
        response = TrafficFlowResponse(data=mock_flow_response)
        speeds = response.free_flow_speeds
        assert len(speeds) == 2
        assert speeds == [60.0, 50.0]
    
    def test_free_flow_speeds_property_missing(self):
        """Test free_flow_speeds when freeFlowSpeed is missing"""
        data = {"flows": [{"other": "data"}]}
        response = TrafficFlowResponse(data=data)
        assert response.free_flow_speeds == []
    
    def test_expected_speeds_property(self, mock_flow_response):
        """Test expected_speeds property"""
        response = TrafficFlowResponse(data=mock_flow_response)
        speeds = response.expected_speeds
        assert len(speeds) == 2
        assert speeds == [45.0, 30.0]
    
    def test_expected_speeds_property_missing(self):
        """Test expected_speeds when expectedSpeed is missing"""
        data = {"flows": [{"other": "data"}]}
        response = TrafficFlowResponse(data=data)
        assert response.expected_speeds == []


class TestTrafficIncidentResponse:
    """Test TrafficIncidentResponse model"""
    
    def test_init_with_data(self, mock_incidents_response):
        """Test TrafficIncidentResponse initialization"""
        response = TrafficIncidentResponse(data=mock_incidents_response)
        assert response.data == mock_incidents_response
        assert response.raw_response == mock_incidents_response
    
    def test_incidents_property(self, mock_incidents_response):
        """Test incidents property"""
        response = TrafficIncidentResponse(data=mock_incidents_response)
        incidents = response.incidents
        assert len(incidents) == 2
        assert incidents[0]["type"] == "accident"
    
    def test_incidents_property_empty(self):
        """Test incidents property with empty data"""
        response = TrafficIncidentResponse(data={})
        assert response.incidents == []
    
    def test_incident_count_property(self, mock_incidents_response):
        """Test incident_count property"""
        response = TrafficIncidentResponse(data=mock_incidents_response)
        assert response.incident_count == 2
    
    def test_incident_count_property_empty(self):
        """Test incident_count with no incidents"""
        response = TrafficIncidentResponse(data={})
        assert response.incident_count == 0
    
    def test_get_incidents_by_type(self, mock_incidents_response):
        """Test get_incidents_by_type method"""
        response = TrafficIncidentResponse(data=mock_incidents_response)
        accidents = response.get_incidents_by_type("accident")
        assert len(accidents) == 1
        assert accidents[0]["type"] == "accident"
    
    def test_get_incidents_by_type_no_matches(self, mock_incidents_response):
        """Test get_incidents_by_type with no matches"""
        response = TrafficIncidentResponse(data=mock_incidents_response)
        no_matches = response.get_incidents_by_type("nonexistent")
        assert len(no_matches) == 0
    
    def test_get_incidents_by_type_missing_type_key(self):
        """Test get_incidents_by_type when type key is missing"""
        data = {"incidents": [{"other": "data"}]}
        response = TrafficIncidentResponse(data=data)
        results = response.get_incidents_by_type("accident")
        assert len(results) == 0
    
    def test_get_critical_incidents(self, mock_incidents_response):
        """Test get_critical_incidents method"""
        response = TrafficIncidentResponse(data=mock_incidents_response)
        critical = response.get_critical_incidents()
        assert len(critical) == 1
        assert critical[0]["criticality"] == "critical"
    
    def test_get_critical_incidents_no_matches(self):
        """Test get_critical_incidents with no critical incidents"""
        data = {
            "incidents": [
                {"criticality": "minor"},
                {"criticality": "low"}
            ]
        }
        response = TrafficIncidentResponse(data=data)
        critical = response.get_critical_incidents()
        assert len(critical) == 0
    
    def test_get_critical_incidents_missing_criticality(self):
        """Test get_critical_incidents when criticality key is missing"""
        data = {"incidents": [{"other": "data"}]}
        response = TrafficIncidentResponse(data=data)
        critical = response.get_critical_incidents()
        assert len(critical) == 0
    
    def test_get_critical_incidents_case_insensitive(self):
        """Test get_critical_incidents is case insensitive"""
        data = {
            "incidents": [
                {"criticality": "CRITICAL"},
                {"criticality": "Critical"}
            ]
        }
        response = TrafficIncidentResponse(data=data)
        critical = response.get_critical_incidents()
        assert len(critical) == 2


class TestAvailabilityResponse:
    """Test AvailabilityResponse model"""
    
    def test_init_with_data(self, mock_availability_response):
        """Test AvailabilityResponse initialization"""
        response = AvailabilityResponse(data=mock_availability_response)
        assert response.data == mock_availability_response
        assert response.raw_response == mock_availability_response
    
    def test_available_property_true(self, mock_availability_response):
        """Test available property when True"""
        response = AvailabilityResponse(data=mock_availability_response)
        assert response.available is True
    
    def test_available_property_false(self):
        """Test available property when False"""
        data = {"available": False}
        response = AvailabilityResponse(data=data)
        assert response.available is False
    
    def test_available_property_missing(self):
        """Test available property when key is missing"""
        response = AvailabilityResponse(data={})
        assert response.available is False
    
    def test_coverage_areas_property(self, mock_availability_response):
        """Test coverage_areas property"""
        response = AvailabilityResponse(data=mock_availability_response)
        coverage = response.coverage_areas
        assert len(coverage) == 1
        assert coverage[0]["country"] == "GB"
    
    def test_coverage_areas_property_empty(self):
        """Test coverage_areas property with empty data"""
        response = AvailabilityResponse(data={})
        assert response.coverage_areas == []
    
    def test_coverage_areas_property_missing_key(self):
        """Test coverage_areas when key is missing"""
        response = AvailabilityResponse(data={"other": "data"})
        assert response.coverage_areas == []

