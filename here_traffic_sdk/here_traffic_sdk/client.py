"""
Main client for HERE Traffic API
Provides unified interface for all API versions
"""

from typing import Optional
from .auth import AuthClient, AuthMethod
from .config import HereTrafficConfig
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
        config: Optional[HereTrafficConfig] = None,
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
        self.config = config or HereTrafficConfig.from_env()
        self.auth_client = AuthClient(
            api_key=api_key,
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            auth_method=auth_method,
            config=self.config,
        )
        
        # Initialize API clients
        self.v7 = TrafficAPIv7(self.auth_client, config=self.config)
        self.v6 = TrafficAPIv6(self.auth_client, config=self.config)
        self.v3 = TrafficAPIv3(self.auth_client, config=self.config)
    
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

