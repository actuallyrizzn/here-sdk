"""
SDK-specific exception types and helpers.

These classes standardize error message formatting while remaining compatible
with callers that already catch `ValueError` or `requests.HTTPError`.
"""

from __future__ import annotations

from typing import Optional

import requests


class HereTrafficSDKError(Exception):
    """Base exception for all SDK-defined errors."""


class HereTrafficAuthError(ValueError, HereTrafficSDKError):
    """Raised when required auth inputs are missing/invalid."""


class HereTrafficHTTPError(requests.HTTPError, HereTrafficSDKError):
    """Raised for HTTP failures in SDK requests."""


def raise_for_status_with_context(
    *,
    response: requests.Response,
    method: str,
    url: str,
    prefix: str = "HERE_TRAFFIC_SDK_HTTP_ERROR",
) -> None:
    """
    Like `response.raise_for_status()` but re-raises with a consistent message.
    """
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        status: Optional[int] = getattr(getattr(exc, "response", None), "status_code", None)
        status_part = f"{status}" if status is not None else "unknown_status"
        msg = f"{prefix}: {method.upper()} {url} failed ({status_part}): {exc}"
        raise HereTrafficHTTPError(msg) from exc

