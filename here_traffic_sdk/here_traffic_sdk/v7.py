"""
HERE Traffic API v7 Client
Current version of the Traffic API
"""

from typing import Dict, Any, Optional
import requests
from .auth import AuthClient
from .http import HttpConfig, get_json
from .models import (
    LocationReference,
    GeospatialFilter,
    TrafficFlowResponse,
    TrafficIncidentResponse,
    AvailabilityResponse,
)


class TrafficAPIv7:
    """
    Client for HERE Traffic API v7
    
    Provides access to:
    - Traffic flow data
    - Traffic incident data
    - API availability information
    """
    
    BASE_URL = "https://data.traffic.hereapi.com/v7"
    
    def __init__(
        self,
        auth_client: AuthClient,
        *,
        session: Optional[requests.Session] = None,
        http_config: Optional[HttpConfig] = None,
    ):
        """
        Initialize Traffic API v7 client
        
        Args:
            auth_client: Authenticated AuthClient instance
        """
        self.auth_client = auth_client
        self.session = session or requests.Session()
        self._owns_session = session is None
        self.http_config = http_config or HttpConfig()

    def close(self):
        """Close the underlying HTTP session if owned by this client."""
        if self._owns_session and self.session is not None:
            self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
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
        params = {
            "locationReferencing": location_referencing.value,
            "in": geospatial_filter,
            **self.auth_client.get_auth_params(),
            **kwargs
        }
        
        headers = self.auth_client.get_auth_headers()

        payload, request_id = get_json(
            session=self.session,
            url=f"{self.BASE_URL}/flow",
            params=params,
            headers=headers,
            config=self.http_config,
        )

        return TrafficFlowResponse(data=payload, raw_response=payload, request_id=request_id)
    
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
        params = {
            "locationReferencing": location_referencing.value,
            "in": geospatial_filter,
            **self.auth_client.get_auth_params(),
            **kwargs
        }
        
        headers = self.auth_client.get_auth_headers()

        payload, request_id = get_json(
            session=self.session,
            url=f"{self.BASE_URL}/incidents",
            params=params,
            headers=headers,
            config=self.http_config,
        )

        return TrafficIncidentResponse(data=payload, raw_response=payload, request_id=request_id)
    
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
            **kwargs
        }
        
        headers = self.auth_client.get_auth_headers()

        payload, request_id = get_json(
            session=self.session,
            url=f"{self.BASE_URL}/availability",
            params=params,
            headers=headers,
            config=self.http_config,
        )

        return AvailabilityResponse(data=payload, raw_response=payload, request_id=request_id)

