"""
HERE Traffic API v3 Client
Legacy version maintained for backward compatibility
"""

from typing import Optional, Dict, Any
import requests
from .auth import AuthClient
from . import constants
from .exceptions import raise_for_status_with_context
from .models import TrafficFlowResponse


class TrafficAPIv3:
    """
    Client for HERE Traffic API v3 (Legacy)
    
    Note: This is a very old version. New implementations should use v7.
    Maintained for backward compatibility only.
    """
    
    BASE_URL = constants.BASE_URL_V3
    
    def __init__(self, auth_client: AuthClient):
        """
        Initialize Traffic API v3 client
        
        Args:
            auth_client: Authenticated AuthClient instance
        """
        self.auth_client = auth_client
        self.session = requests.Session()
        # Identify the SDK in outbound requests.
        self.session.headers.update({"User-Agent": constants.DEFAULT_USER_AGENT})
    
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
        raise_for_status_with_context(response=response, method="GET", url=f"{self.BASE_URL}/flow")
        
        return TrafficFlowResponse(data=response.json(), raw_response=response.json())

