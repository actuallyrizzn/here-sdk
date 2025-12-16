"""
HERE Traffic API v3 Client
Legacy version maintained for backward compatibility
"""

from typing import Optional, Dict, Any
import requests
from .auth import AuthClient
from .models import TrafficFlowResponse


class TrafficAPIv3:
    """
    Client for HERE Traffic API v3 (Legacy)
    
    Note: This is a very old version. New implementations should use v7.
    Maintained for backward compatibility only.
    """
    
    BASE_URL = "https://traffic.api.here.com/v3"
    
    def __init__(self, auth_client: AuthClient):
        """
        Initialize Traffic API v3 client
        
        Args:
            auth_client: Authenticated AuthClient instance
        """
        self.auth_client = auth_client
        self.session = requests.Session()

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self.session.close()
    
    def get_flow(
        self,
        **kwargs
    ) -> TrafficFlowResponse:
        """
        Get traffic flow data (v3)
        
        Args:
            **kwargs: Query parameters (specific parameters depend on v3 API specification)
            
        Returns:
            TrafficFlowResponse with flow data
            
        Note: v3 API parameters may differ from v6.3 and v7.
        Refer to HERE documentation for v3-specific parameters.
        """
        params = {
            **self.auth_client.get_auth_params(),
            **kwargs
        }
        
        headers = self.auth_client.get_auth_headers()
        
        response = self.session.get(
            f"{self.BASE_URL}/flow",
            params=params,
            headers=headers
        )
        response.raise_for_status()
        
        return TrafficFlowResponse(data=response.json(), raw_response=response.json())

