"""
Authentication client for HERE APIs
Supports API Key and OAuth 2.0 authentication
"""

from enum import Enum
from typing import Optional
import requests
from datetime import datetime, timedelta
from .http import HttpConfig, _has_header, _redact_headers

from . import constants
from .exceptions import HereTrafficAuthError, raise_for_status_with_context


class AuthMethod(Enum):
    """Authentication method enumeration"""
    API_KEY = "api_key"
    OAUTH = "oauth"


class AuthClient:
    """
    Authentication client for HERE APIs
    
    Supports both API Key and OAuth 2.0 authentication methods.
    """
    
    OAUTH_TOKEN_URL = constants.OAUTH_TOKEN_URL
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        access_key_id: Optional[str] = None,
        access_key_secret: Optional[str] = None,
        auth_method: AuthMethod = AuthMethod.API_KEY,
        *,
        http_config: Optional[HttpConfig] = None,
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
        self.http_config = http_config or HttpConfig()
        
        # OAuth token management
        self._oauth_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None
    
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
                raise HereTrafficAuthError(
                    "HERE_TRAFFIC_SDK_AUTH_ERROR: API key is required for API key authentication"
                )
            return {"apiKey": self.api_key}
        return {}
    
    def _get_oauth_token(self) -> str:
        """
        Get OAuth access token, refreshing if necessary
        
        Returns:
            OAuth access token string
        """
        # Check if we have a valid token
        if self._oauth_token and self._token_expires_at:
            if datetime.now() < self._token_expires_at - timedelta(minutes=5):
                return self._oauth_token
        
        # Request new token
        if not self.access_key_id or not self.access_key_secret:
            raise HereTrafficAuthError(
                "HERE_TRAFFIC_SDK_AUTH_ERROR: OAuth credentials (access_key_id and access_key_secret) are required for OAuth authentication"
            )
        
        headers = self._oauth_request_headers()
        headers["Content-Type"] = constants.CONTENT_TYPE_FORM_URLENCODED
        headers["User-Agent"] = constants.DEFAULT_USER_AGENT
        
        response = requests.post(
            self.OAUTH_TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": self.access_key_id,
                "client_secret": self.access_key_secret,
            },
            headers=headers,
            timeout=self.http_config.timeout,
            verify=self.http_config.verify,
        )
        
        raise_for_status_with_context(
            response=response, method="POST", url=self.OAUTH_TOKEN_URL, prefix="HERE_TRAFFIC_SDK_OAUTH_ERROR"
        )
        try:
            token_data = response.json()
        except ValueError as e:
            raise ValueError(f"Invalid JSON response from OAuth token endpoint: {self.OAUTH_TOKEN_URL}") from e
        
        self._oauth_token = token_data["access_token"]
        expires_in = token_data.get("expires_in", 3600)
        self._token_expires_at = datetime.now() + timedelta(seconds=expires_in)

        return self._oauth_token

    def _oauth_request_headers(self) -> dict:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        # Correlate token requests too, so users can debug auth issues.
        if not _has_header(headers, "X-Request-Id"):
            headers["X-Request-Id"] = self.http_config.request_id_factory()

        if self.http_config.enable_logging:
            self.http_config.logger.debug(
                "HERE SDK OAuth token request",
                extra={
                    "method": "POST",
                    "url": self.OAUTH_TOKEN_URL,
                    "headers": _redact_headers(headers),
                },
            )
        return headers
    
    def refresh_token(self):
        """Manually refresh OAuth token"""
        self._oauth_token = None
        self._token_expires_at = None
        self._get_oauth_token()

