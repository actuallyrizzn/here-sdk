"""
HERE Traffic API v3 Client
Legacy version maintained for backward compatibility
"""

from typing import Any, Dict, Optional
import requests
from .auth import AuthClient
from . import constants
from .exceptions import raise_for_status_with_context
from .http import HttpConfig, get_json
from .models import TrafficFlowResponse
try:
    from .validation import sanitize_query_params
except ImportError:
    # Fallback if validation module not available
    def sanitize_query_params(params):
        return params


class TrafficAPIv3:
    """
    Client for HERE Traffic API v3 (Legacy)
    
    Note: This is a very old version. New implementations should use v7.
    Maintained for backward compatibility only.
    """
    
    BASE_URL = constants.BASE_URL_V3
    
    def __init__(
        self,
        auth_client: AuthClient,
        *,
        session: Optional[requests.Session] = None,
        http_config: Optional[HttpConfig] = None,
    ):
        """
        Initialize Traffic API v3 client
        
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

        payload, request_id = get_json(
            session=self.session,
            url=f"{self.BASE_URL}/flow",
            params=params,
            headers=headers,
            config=self.http_config,
        )

        return TrafficFlowResponse(data=payload, raw_response=payload, request_id=request_id)

