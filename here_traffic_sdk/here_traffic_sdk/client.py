"""
Main client for HERE Traffic API
Provides unified interface for all API versions
"""

from typing import Callable, Optional, Sequence
import logging
import requests
from .auth import AuthClient, AuthMethod
from .http import HttpConfig, RetryConfig, TimeoutType, VerifyType
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
        timeout: Optional[TimeoutType] = 30.0,
        verify_ssl: VerifyType = True,
        enable_logging: bool = False,
        logger: Optional[logging.Logger] = None,
        request_id_factory: Optional[Callable[[], str]] = None,
        max_retries: int = 3,
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
        base = HttpConfig()
        retry_cfg = retry_config or RetryConfig(
            max_retries=max_retries,
            timeout=float(timeout) if isinstance(timeout, (int, float)) else 30.0,
            backoff_factor=backoff_factor,
            max_backoff=max_backoff,
            retry_statuses=tuple(retry_statuses),
        )
        self.http_config = HttpConfig(
            timeout=timeout,
            verify=verify_ssl,
            enable_logging=enable_logging,
            request_id_factory=request_id_factory or base.request_id_factory,
            logger=logger or base.logger,
            retry_config=retry_cfg,
        )

        self.auth_client = AuthClient(
            api_key=api_key,
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            auth_method=auth_method,
            http_config=self.http_config,
        )

        # Shared session for all API versions (closed via close()).
        self._session = requests.Session()
        
        # Initialize API clients
        self.v7 = TrafficAPIv7(self.auth_client, session=self._session, http_config=self.http_config)
        self.v6 = TrafficAPIv6(self.auth_client, session=self._session, http_config=self.http_config)
        self.v3 = TrafficAPIv3(self.auth_client, session=self._session, http_config=self.http_config)

    def close(self):
        """Close the underlying shared HTTP session."""
        if self._session is not None:
            self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
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

