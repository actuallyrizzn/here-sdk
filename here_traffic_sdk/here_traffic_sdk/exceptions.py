"""
SDK exception hierarchy for HERE Traffic SDK.

The goal is to provide structured, actionable errors instead of raw `requests.HTTPError`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


class HereSDKError(Exception):
    """Base exception for all SDK errors."""


@dataclass
class HereAPIError(HereSDKError):
    """Base exception for HTTP/API errors."""

    message: str
    status_code: Optional[int] = None
    url: Optional[str] = None
    response_text: Optional[str] = None
    response_json: Optional[Dict[str, Any]] = None

    def __str__(self) -> str:
        parts = [self.message]
        if self.status_code is not None:
            parts.append(f"status={self.status_code}")
        if self.url:
            parts.append(f"url={self.url}")
        if len(parts) == 1:
            return parts[0]
        return parts[0] + " (" + ", ".join(parts[1:]) + ")"


class HereAuthenticationError(HereAPIError):
    """Authentication/authorization error (401/403)."""


class HereRateLimitError(HereAPIError):
    """Rate limiting error (429)."""


class HereNotFoundError(HereAPIError):
    """Not found error (404)."""


class HereClientError(HereAPIError):
    """Other 4xx errors."""


class HereServerError(HereAPIError):
    """5xx errors."""


class HereConnectionError(HereSDKError):
    """Networking/transport error (timeouts, DNS, etc.)."""

