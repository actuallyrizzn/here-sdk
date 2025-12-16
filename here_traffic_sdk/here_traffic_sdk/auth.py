"""
Authentication client for HERE APIs
Supports API Key and OAuth 2.0 authentication
"""

from enum import Enum
from typing import Optional
import threading
import requests
from datetime import datetime, timedelta

from .config import HereTrafficConfig
from .exceptions import HereConnectionError
from .http import raise_for_here_status


class AuthMethod(Enum):
    """Authentication method enumeration"""
    API_KEY = "api_key"
    OAUTH = "oauth"


class AuthClient:
    """
    Authentication client for HERE APIs
    
    Supports both API Key and OAuth 2.0 authentication methods.
    """
    
    # Default (may be overridden via HereTrafficConfig)
    OAUTH_TOKEN_URL = "https://account.api.here.com/oauth2/token"
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        access_key_id: Optional[str] = None,
        access_key_secret: Optional[str] = None,
        auth_method: AuthMethod = AuthMethod.API_KEY,
        config: Optional[HereTrafficConfig] = None,
    ):
        """
        Initialize authentication client
        
        Args:
            api_key: HERE API key (for API key authentication)
            access_key_id: OAuth Access Key ID (for OAuth authentication)
            access_key_secret: OAuth Access Key Secret (for OAuth authentication)
            auth_method: Authentication method to use
        """
        self.api_key = api_key
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.auth_method = auth_method
        self.config = config or HereTrafficConfig.from_env()
        
        # OAuth token management
        self._oauth_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None
        self._token_lock = threading.Lock()
    
    def get_auth_headers(self) -> dict:
        """
        Get authentication headers for API requests
        
        Returns:
            Dictionary with authentication headers
        """
        if self.auth_method == AuthMethod.OAUTH:
            token = self._get_oauth_token()
            return {"Authorization": f"Bearer {token}"}
        return {}
    
    def get_auth_params(self) -> dict:
        """
        Get authentication query parameters for API requests
        
        Returns:
            Dictionary with authentication query parameters
        """
        if self.auth_method == AuthMethod.API_KEY:
            if not self.api_key:
                raise ValueError("API key is required for API key authentication")
            return {"apiKey": self.api_key}
        return {}
    
    def _get_oauth_token(self) -> str:
        """
        Get OAuth access token, refreshing if necessary
        
        Returns:
            OAuth access token string
        """
        # Fast-path check (unsynchronized) to avoid lock overhead in the common case.
        if self._oauth_token and self._token_expires_at:
            if datetime.now() < self._token_expires_at - timedelta(minutes=5):
                return self._oauth_token

        with self._token_lock:
            # Double-check inside lock to avoid token thundering herd.
            if self._oauth_token and self._token_expires_at:
                if datetime.now() < self._token_expires_at - timedelta(minutes=5):
                    return self._oauth_token

            # Request new token
            if not self.access_key_id or not self.access_key_secret:
                raise ValueError(
                    "OAuth credentials (access_key_id and access_key_secret) are required for OAuth authentication"
                )

            try:
                response = requests.post(
                    self.config.oauth_token_url or self.OAUTH_TOKEN_URL,
                    data={
                        "grant_type": "client_credentials",
                        "client_id": self.access_key_id,
                        "client_secret": self.access_key_secret,
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=self.config.http_timeout_seconds,
                )
            except requests.RequestException as exc:
                raise HereConnectionError(f"Failed to request OAuth token: {exc}") from exc

            raise_for_here_status(response)
            token_data = response.json()

            self._oauth_token = token_data["access_token"]
            expires_in = token_data.get("expires_in", 3600)
            self._token_expires_at = datetime.now() + timedelta(seconds=expires_in)

            return self._oauth_token
    
    def refresh_token(self):
        """Manually refresh OAuth token"""
        with self._token_lock:
            self._oauth_token = None
            self._token_expires_at = None
        self._get_oauth_token()

