"""
HERE Traffic API v6.3 Client
Legacy version maintained for backward compatibility
"""

from typing import Optional, Dict, Any
import requests
from .auth import AuthClient
from .config import HereTrafficConfig
from .exceptions import HereConnectionError
from .http import raise_for_here_status
from .models import TrafficFlowResponse, TrafficIncidentResponse
from .validation import sanitize_query_params, validate_bbox_string


class TrafficAPIv6:
    """
    Client for HERE Traffic API v6.3 (Legacy)
    
    Note: This is a legacy version. New implementations should use v7.
    Maintained for backward compatibility.
    """
    
    BASE_URL = "https://traffic.api.here.com/traffic/6.3"
    
    def __init__(self, auth_client: AuthClient, config: Optional[HereTrafficConfig] = None):
        """
        Initialize Traffic API v6.3 client
        
        Args:
            auth_client: Authenticated AuthClient instance
        """
        self.auth_client = auth_client
        self.config = config or getattr(auth_client, "config", None) or HereTrafficConfig.from_env()
        self.session = requests.Session()
        self.base_url = self.config.v6_base_url or self.BASE_URL
    
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
        
        try:
            response = self.session.get(
                f"{self.base_url}/flow.json",
                params=params,
                headers=headers,
                timeout=self.config.http_timeout_seconds,
            )
        except requests.RequestException as exc:
            raise HereConnectionError(f"Failed to call HERE Traffic v6.3 flow endpoint: {exc}") from exc
        raise_for_here_status(response)
        
        return TrafficFlowResponse(data=response.json(), raw_response=response.json())
    
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
        
        try:
            response = self.session.get(
                f"{self.base_url}/incidents.json",
                params=params,
                headers=headers,
                timeout=self.config.http_timeout_seconds,
            )
        except requests.RequestException as exc:
            raise HereConnectionError(f"Failed to call HERE Traffic v6.3 incidents endpoint: {exc}") from exc
        raise_for_here_status(response)
        
        return TrafficIncidentResponse(data=response.json(), raw_response=response.json())
    
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

