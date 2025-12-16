"""
HERE Traffic API v6.3 Client
Legacy version maintained for backward compatibility
"""

from typing import Any, Dict, Optional
import requests
from .auth import AuthClient
from . import constants
from .exceptions import raise_for_status_with_context
from .http import HttpConfig, get_json
from .models import TrafficFlowResponse, TrafficIncidentResponse
try:
    from .validation import sanitize_query_params, validate_bbox_string
except ImportError:
    # Fallback if validation module not available
    def sanitize_query_params(params):
        return params
    def validate_bbox_string(bbox):
        return bbox


class TrafficAPIv6:
    """
    Client for HERE Traffic API v6.3 (Legacy)
    
    Note: This is a legacy version. New implementations should use v7.
    Maintained for backward compatibility.
    """
    
    BASE_URL = constants.BASE_URL_V6
    
    def __init__(
        self,
        auth_client: AuthClient,
        *,
        session: Optional[requests.Session] = None,
        http_config: Optional[HttpConfig] = None,
    ):
        """
        Initialize Traffic API v6.3 client
        
        Args:
            auth_client: Authenticated AuthClient instance
        """
        self.auth_client = auth_client
        self.session = session or requests.Session()
        self._owns_session = session is None
        self.http_config = http_config or HttpConfig()
        # Identify the SDK in outbound requests.
        self.session.headers.update({"User-Agent": constants.DEFAULT_USER_AGENT})

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
        bbox: str,
        **kwargs
    ) -> TrafficFlowResponse:
        """
        Get traffic flow data (v6.3)
        
        Args:
            bbox: Bounding box in format "LAT1,LON1;LAT2,LON2"
            **kwargs: Additional query parameters
            
        Returns:
            TrafficFlowResponse with flow data
            
        Example:
            >>> client = TrafficAPIv6(auth_client)
            >>> response = client.get_flow("51.5,-0.13;51.51,-0.12")
        """
        bbox = validate_bbox_string(bbox)
        params = {
            "bbox": bbox,
            **self.auth_client.get_auth_params(),
            **sanitize_query_params(kwargs),
        }
        
        headers = self.auth_client.get_auth_headers()

        payload, request_id = get_json(
            session=self.session,
            url=f"{self.BASE_URL}/flow.json",
            params=params,
            headers=headers,
            config=self.http_config,
        )

        return TrafficFlowResponse(data=payload, raw_response=payload, request_id=request_id)
    
    def get_flow_bbox(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
        **kwargs
    ) -> TrafficFlowResponse:
        """
        Get traffic flow data for a bounding box (v6.3)
        
        Args:
            lat1: First latitude coordinate
            lon1: First longitude coordinate
            lat2: Second latitude coordinate
            lon2: Second longitude coordinate
            **kwargs: Additional query parameters
            
        Returns:
            TrafficFlowResponse with flow data
        """
        bbox_str = f"{lat1},{lon1};{lat2},{lon2}"
        return self.get_flow(bbox_str, **kwargs)
    
    def get_incidents(
        self,
        bbox: str,
        **kwargs
    ) -> TrafficIncidentResponse:
        """
        Get traffic incident data (v6.3)
        
        Args:
            bbox: Bounding box in format "LAT1,LON1;LAT2,LON2"
            **kwargs: Additional query parameters
            
        Returns:
            TrafficIncidentResponse with incident data
            
        Example:
            >>> client = TrafficAPIv6(auth_client)
            >>> response = client.get_incidents("51.5,-0.13;51.51,-0.12")
        """
        bbox = validate_bbox_string(bbox)
        params = {
            "bbox": bbox,
            **self.auth_client.get_auth_params(),
            **sanitize_query_params(kwargs),
        }
        
        headers = self.auth_client.get_auth_headers()

        payload, request_id = get_json(
            session=self.session,
            url=f"{self.BASE_URL}/incidents.json",
            params=params,
            headers=headers,
            config=self.http_config,
        )

        return TrafficIncidentResponse(data=payload, raw_response=payload, request_id=request_id)
    
    def get_incidents_bbox(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
        **kwargs
    ) -> TrafficIncidentResponse:
        """
        Get traffic incident data for a bounding box (v6.3)
        
        Args:
            lat1: First latitude coordinate
            lon1: First longitude coordinate
            lat2: Second latitude coordinate
            lon2: Second longitude coordinate
            **kwargs: Additional query parameters
            
        Returns:
            TrafficIncidentResponse with incident data
        """
        bbox_str = f"{lat1},{lon1};{lat2},{lon2}"
        return self.get_incidents(bbox_str, **kwargs)

