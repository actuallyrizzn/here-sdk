"""
Data models for HERE Traffic API responses
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class LocationReference(str, Enum):
    """Location referencing methods"""
    SHAPE = "shape"
    TMC = "tmc"
    OLR = "olr"


@dataclass
class GeospatialFilter:
    """Geospatial filter for API requests"""
    
    @staticmethod
    def circle(latitude: float, longitude: float, radius_meters: int) -> str:
        """
        Create a circle filter
        
        Args:
            latitude: Center latitude
            longitude: Center longitude
            radius_meters: Radius in meters
            
        Returns:
            Circle filter string
        """
        return f"circle:{latitude},{longitude};r={radius_meters}"
    
    @staticmethod
    def bbox(lat1: float, lon1: float, lat2: float, lon2: float) -> str:
        """
        Create a bounding box filter
        
        Args:
            lat1: First latitude coordinate
            lon1: First longitude coordinate
            lat2: Second latitude coordinate
            lon2: Second longitude coordinate
            
        Returns:
            Bounding box filter string
        """
        return f"bbox:{lat1},{lon1};{lat2},{lon2}"
    
    @staticmethod
    def corridor(encoded_polyline: str) -> str:
        """
        Create a corridor/polyline filter
        
        Args:
            encoded_polyline: Encoded polyline string
            
        Returns:
            Corridor filter string
        """
        return f"corridor:{encoded_polyline}"


@dataclass
class TrafficFlowResponse:
    """Response model for traffic flow data"""
    data: Dict[str, Any]
    raw_response: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Parse response data"""
        if self.raw_response is None:
            self.raw_response = self.data
    
    @property
    def flows(self) -> List[Dict[str, Any]]:
        """Get list of traffic flow data"""
        return self.data.get("flows", [])
    
    @property
    def free_flow_speeds(self) -> List[float]:
        """Get list of free-flow speeds"""
        speeds = []
        for flow in self.flows:
            if "freeFlowSpeed" in flow:
                speeds.append(flow["freeFlowSpeed"])
        return speeds
    
    @property
    def expected_speeds(self) -> List[float]:
        """Get list of expected speeds"""
        speeds = []
        for flow in self.flows:
            if "expectedSpeed" in flow:
                speeds.append(flow["expectedSpeed"])
        return speeds


@dataclass
class TrafficIncidentResponse:
    """Response model for traffic incident data"""
    data: Dict[str, Any]
    raw_response: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Parse response data"""
        if self.raw_response is None:
            self.raw_response = self.data
    
    @property
    def incidents(self) -> List[Dict[str, Any]]:
        """Get list of traffic incidents"""
        return self.data.get("incidents", [])
    
    @property
    def incident_count(self) -> int:
        """Get total number of incidents"""
        return len(self.incidents)
    
    def get_incidents_by_type(self, incident_type: str) -> List[Dict[str, Any]]:
        """
        Get incidents filtered by type
        
        Args:
            incident_type: Type of incident to filter by
            
        Returns:
            List of incidents matching the type
        """
        return [inc for inc in self.incidents if inc.get("type") == incident_type]
    
    def get_critical_incidents(self) -> List[Dict[str, Any]]:
        """Get only critical incidents"""
        return [inc for inc in self.incidents if inc.get("criticality", "").lower() == "critical"]


@dataclass
class AvailabilityResponse:
    """Response model for API availability data"""
    data: Dict[str, Any]
    raw_response: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Parse response data"""
        if self.raw_response is None:
            self.raw_response = self.data
    
    @property
    def available(self) -> bool:
        """Check if API is available"""
        return self.data.get("available", False)
    
    @property
    def coverage_areas(self) -> List[Dict[str, Any]]:
        """Get list of coverage areas"""
        return self.data.get("coverage", [])

