"""
HERE Traffic API v3 Client
Legacy version maintained for backward compatibility
"""

from typing import Optional, Dict, Any
import requests
from .auth import AuthClient
from .config import HereTrafficConfig
from .exceptions import HereConnectionError
from .http import raise_for_here_status
from .models import TrafficFlowResponse
from .validation import sanitize_query_params


class TrafficAPIv3:
    """
    Client for HERE Traffic API v3 (Legacy)
    
    Note: This is a very old version. New implementations should use v7.
    Maintained for backward compatibility only.
    """
    
    BASE_URL = "https://traffic.api.here.com/v3"
    
    def __init__(self, auth_client: AuthClient, config: Optional[HereTrafficConfig] = None):
        """
        Initialize Traffic API v3 client
        
        Args:
            auth_client: Authenticated AuthClient instance
        """
        self.auth_client = auth_client
        self.config = config or getattr(auth_client, "config", None) or HereTrafficConfig.from_env()
        self.session = requests.Session()
        self.base_url = self.config.v3_base_url or self.BASE_URL
    
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
            raise HereConnectionError(f"Failed to call HERE Traffic v3 flow endpoint: {exc}") from exc
        raise_for_here_status(response)
        
        return TrafficFlowResponse(data=response.json(), raw_response=response.json())

