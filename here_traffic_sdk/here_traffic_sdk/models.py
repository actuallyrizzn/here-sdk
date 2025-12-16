"""
Data models for HERE Traffic API responses
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum

from .validation import (
    validate_encoded_polyline,
    validate_latitude,
    validate_longitude,
    validate_radius_meters,
)


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
        lat = validate_latitude(latitude)
        lon = validate_longitude(longitude)
        radius = validate_radius_meters(radius_meters)
        return f"circle:{lat},{lon};r={radius}"
    
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
        a_lat = validate_latitude(lat1)
        a_lon = validate_longitude(lon1)
        b_lat = validate_latitude(lat2)
        b_lon = validate_longitude(lon2)
        return f"bbox:{a_lat},{a_lon};{b_lat},{b_lon}"
    
    @staticmethod
    def corridor(encoded_polyline: str) -> str:
        """
        Create a corridor/polyline filter
        
        Args:
            encoded_polyline: Encoded polyline string
            
        Returns:
            Corridor filter string
        """
        polyline = validate_encoded_polyline(encoded_polyline)
        return f"corridor:{polyline}"


def _coerce_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        s = value.strip().lower()
        if s in {"true", "1", "yes", "y", "on"}:
            return True
        if s in {"false", "0", "no", "n", "off"}:
            return False
    return False


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
                coerced = _coerce_float(flow.get("freeFlowSpeed"))
                if coerced is not None:
                    speeds.append(coerced)
        return speeds
    
    @property
    def expected_speeds(self) -> List[float]:
        """Get list of expected speeds"""
        speeds = []
        for flow in self.flows:
            if "expectedSpeed" in flow:
                coerced = _coerce_float(flow.get("expectedSpeed"))
                if coerced is not None:
                    speeds.append(coerced)
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
        return _coerce_bool(self.data.get("available", False))
    
    @property
    def coverage_areas(self) -> List[Dict[str, Any]]:
        """Get list of coverage areas"""
        return self.data.get("coverage", [])

