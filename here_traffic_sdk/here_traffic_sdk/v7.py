"""
HERE Traffic API v7 Client
Current version of the Traffic API
"""

from typing import Optional, Dict, Any
import requests
from .auth import AuthClient
from .config import HereTrafficConfig
from .exceptions import HereConnectionError
from .http import raise_for_here_status
from .models import (
    LocationReference,
    GeospatialFilter,
    TrafficFlowResponse,
    TrafficIncidentResponse,
    AvailabilityResponse,
)
from .validation import sanitize_query_params, validate_geospatial_filter


class TrafficAPIv7:
    """
    Client for HERE Traffic API v7
    
    Provides access to:
    - Traffic flow data
    - Traffic incident data
    - API availability information
    """
    
    BASE_URL = "https://data.traffic.hereapi.com/v7"
    
    def __init__(self, auth_client: AuthClient, config: Optional[HereTrafficConfig] = None):
        """
        Initialize Traffic API v7 client
        
        Args:
            auth_client: Authenticated AuthClient instance
        """
        self.auth_client = auth_client
        self.config = config or getattr(auth_client, "config", None) or HereTrafficConfig.from_env()
        self.session = requests.Session()
        self.base_url = self.config.v7_base_url or self.BASE_URL
    
    def get_flow(
        self,
        location_referencing: LocationReference,
        geospatial_filter: str,
        **kwargs
    ) -> TrafficFlowResponse:
        """
        Get traffic flow data
        
        Args:
            location_referencing: Location referencing method (shape, tmc, olr)
            geospatial_filter: Geospatial filter (circle, bbox, or corridor)
            **kwargs: Additional query parameters
            
        Returns:
            TrafficFlowResponse with flow data
            
        Example:
            >>> client = TrafficAPIv7(auth_client)
            >>> filter_str = GeospatialFilter.circle(51.50643, -0.12719, 1000)
            >>> response = client.get_flow(LocationReference.SHAPE, filter_str)
        """
        geospatial_filter = validate_geospatial_filter(geospatial_filter)
        params = {
            "locationReferencing": location_referencing.value,
            "in": geospatial_filter,
            **self.auth_client.get_auth_params(),
            **sanitize_query_params(kwargs),
        }
        
        headers = self.auth_client.get_auth_headers()
        
        try:
            response = self.session.get(
                f"{self.base_url}/flow",
                params=params,
                headers=headers,
                timeout=self.config.http_timeout_seconds,
            )
        except requests.RequestException as exc:
            raise HereConnectionError(f"Failed to call HERE Traffic v7 flow endpoint: {exc}") from exc
        raise_for_here_status(response)
        
        return TrafficFlowResponse(data=response.json(), raw_response=response.json())
    
    def get_flow_circle(
        self,
        latitude: float,
        longitude: float,
        radius_meters: int,
        location_referencing: LocationReference = LocationReference.SHAPE,
        **kwargs
    ) -> TrafficFlowResponse:
        """
        Get traffic flow data for a circular area
        
        Args:
            latitude: Center latitude
            longitude: Center longitude
            radius_meters: Radius in meters
            location_referencing: Location referencing method
            **kwargs: Additional query parameters
            
        Returns:
            TrafficFlowResponse with flow data
        """
        filter_str = GeospatialFilter.circle(latitude, longitude, radius_meters)
        return self.get_flow(location_referencing, filter_str, **kwargs)
    
    def get_flow_bbox(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
        location_referencing: LocationReference = LocationReference.SHAPE,
        **kwargs
    ) -> TrafficFlowResponse:
        """
        Get traffic flow data for a bounding box
        
        Args:
            lat1: First latitude coordinate
            lon1: First longitude coordinate
            lat2: Second latitude coordinate
            lon2: Second longitude coordinate
            location_referencing: Location referencing method
            **kwargs: Additional query parameters
            
        Returns:
            TrafficFlowResponse with flow data
        """
        filter_str = GeospatialFilter.bbox(lat1, lon1, lat2, lon2)
        return self.get_flow(location_referencing, filter_str, **kwargs)
    
    def get_incidents(
        self,
        location_referencing: LocationReference,
        geospatial_filter: str,
        **kwargs
    ) -> TrafficIncidentResponse:
        """
        Get traffic incident data
        
        Args:
            location_referencing: Location referencing method (shape, tmc, olr)
            geospatial_filter: Geospatial filter (circle, bbox, or corridor)
            **kwargs: Additional query parameters
            
        Returns:
            TrafficIncidentResponse with incident data
            
        Example:
            >>> client = TrafficAPIv7(auth_client)
            >>> filter_str = GeospatialFilter.circle(51.50643, -0.12719, 1000)
            >>> response = client.get_incidents(LocationReference.SHAPE, filter_str)
        """
        geospatial_filter = validate_geospatial_filter(geospatial_filter)
        params = {
            "locationReferencing": location_referencing.value,
            "in": geospatial_filter,
            **self.auth_client.get_auth_params(),
            **sanitize_query_params(kwargs),
        }
        
        headers = self.auth_client.get_auth_headers()
        
        try:
            response = self.session.get(
                f"{self.base_url}/incidents",
                params=params,
                headers=headers,
                timeout=self.config.http_timeout_seconds,
            )
        except requests.RequestException as exc:
            raise HereConnectionError(f"Failed to call HERE Traffic v7 incidents endpoint: {exc}") from exc
        raise_for_here_status(response)
        
        return TrafficIncidentResponse(data=response.json(), raw_response=response.json())
    
    def get_incidents_circle(
        self,
        latitude: float,
        longitude: float,
        radius_meters: int,
        location_referencing: LocationReference = LocationReference.SHAPE,
        **kwargs
    ) -> TrafficIncidentResponse:
        """
        Get traffic incident data for a circular area
        
        Args:
            latitude: Center latitude
            longitude: Center longitude
            radius_meters: Radius in meters
            location_referencing: Location referencing method
            **kwargs: Additional query parameters
            
        Returns:
            TrafficIncidentResponse with incident data
        """
        filter_str = GeospatialFilter.circle(latitude, longitude, radius_meters)
        return self.get_incidents(location_referencing, filter_str, **kwargs)
    
    def get_incidents_bbox(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
        location_referencing: LocationReference = LocationReference.SHAPE,
        **kwargs
    ) -> TrafficIncidentResponse:
        """
        Get traffic incident data for a bounding box
        
        Args:
            lat1: First latitude coordinate
            lon1: First longitude coordinate
            lat2: Second latitude coordinate
            lon2: Second longitude coordinate
            location_referencing: Location referencing method
            **kwargs: Additional query parameters
            
        Returns:
            TrafficIncidentResponse with incident data
        """
        filter_str = GeospatialFilter.bbox(lat1, lon1, lat2, lon2)
        return self.get_incidents(location_referencing, filter_str, **kwargs)
    
    def get_availability(self, **kwargs) -> AvailabilityResponse:
        """
        Get API availability information
        
        Args:
            **kwargs: Additional query parameters
            
        Returns:
            AvailabilityResponse with availability data
        """
        params = {
            **self.auth_client.get_auth_params(),
            **sanitize_query_params(kwargs),
        }
        
        headers = self.auth_client.get_auth_headers()
        
        try:
            response = self.session.get(
                f"{self.base_url}/availability",
                params=params,
                headers=headers,
                timeout=self.config.http_timeout_seconds,
            )
        except requests.RequestException as exc:
            raise HereConnectionError(f"Failed to call HERE Traffic v7 availability endpoint: {exc}") from exc
        raise_for_here_status(response)
        
        return AvailabilityResponse(data=response.json(), raw_response=response.json())

