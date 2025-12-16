"""
Main client for HERE Traffic API
Provides unified interface for all API versions
"""

from typing import Optional, Sequence
from .auth import AuthClient, AuthMethod
from ._retry import RetryConfig
from .v7 import TrafficAPIv7
from .v6 import TrafficAPIv6
from .v3 import TrafficAPIv3


class HereTrafficClient:
    """
    Main client for HERE Traffic and Incident APIs
    
    Provides unified access to both v7 (current) and v6.3 (legacy) APIs.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        access_key_id: Optional[str] = None,
        access_key_secret: Optional[str] = None,
        auth_method: AuthMethod = AuthMethod.API_KEY,
        *,
        max_retries: int = 3,
        timeout: float = 30.0,
        backoff_factor: float = 0.5,
        max_backoff: float = 8.0,
        retry_statuses: Sequence[int] = (429, 500, 502, 503, 504),
        retry_config: Optional[RetryConfig] = None,
    ):
        """
        Initialize HERE Traffic API client
        
        Args:
            api_key: HERE API key (for API key authentication)
            access_key_id: OAuth Access Key ID (for OAuth authentication)
            access_key_secret: OAuth Access Key Secret (for OAuth authentication)
            auth_method: Authentication method to use (default: API_KEY)
            max_retries: Number of retries after the initial request (default: 3)
            timeout: Per-request timeout in seconds (default: 30.0)
            backoff_factor: Exponential backoff factor (default: 0.5)
            max_backoff: Maximum backoff sleep in seconds (default: 8.0)
            retry_statuses: HTTP statuses to retry (default: 429, 500, 502, 503, 504)
            retry_config: Advanced override for retry configuration (optional)
            
        Example:
            >>> # Using API Key
            >>> client = HereTrafficClient(api_key="YOUR_API_KEY")
            >>> 
            >>> # Using OAuth
            >>> client = HereTrafficClient(
            ...     access_key_id="YOUR_ACCESS_KEY_ID",
            ...     access_key_secret="YOUR_ACCESS_KEY_SECRET",
            ...     auth_method=AuthMethod.OAUTH
            ... )
        """
        self.auth_client = AuthClient(
            api_key=api_key,
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            auth_method=auth_method
        )

        self.retry_config = retry_config or RetryConfig(
            max_retries=max_retries,
            timeout=timeout,
            backoff_factor=backoff_factor,
            max_backoff=max_backoff,
            retry_statuses=tuple(retry_statuses),
        )
        
        # Initialize API clients
        self.v7 = TrafficAPIv7(self.auth_client, retry_config=self.retry_config)
        self.v6 = TrafficAPIv6(self.auth_client, retry_config=self.retry_config)
        self.v3 = TrafficAPIv3(self.auth_client, retry_config=self.retry_config)
    
    @property
    def flow(self):
        """Access to traffic flow endpoints (v7)"""
        return self.v7
    
    @property
    def incidents(self):
        """Access to traffic incident endpoints (v7)"""
        return self.v7
    
    @property
    def availability(self):
        """Access to availability endpoint (v7)"""
        return self.v7

