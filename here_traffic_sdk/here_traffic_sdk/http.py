"""
HTTP helpers for HERE Traffic SDK.

Centralizes:
- query param validation/sanitization (see `validation.py`)
- HTTP status -> SDK exception mapping
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from .exceptions import (
    HereAuthenticationError,
    HereClientError,
    HereNotFoundError,
    HereRateLimitError,
    HereServerError,
)


def _safe_response_payload(response: Any) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    """
    Best-effort extraction of response text and JSON.
    Works with real `requests.Response` and with unit-test mocks.
    """
    text: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

    try:
        text = getattr(response, "text")
    except Exception:
        text = None

    try:
        json_func = getattr(response, "json")
    except Exception:
        json_func = None

    if callable(json_func):
        try:
            maybe = json_func()
            if isinstance(maybe, dict):
                data = maybe
        except Exception:
            data = None

    return text, data


def raise_for_here_status(response: Any) -> None:
    """
    Raise a typed SDK exception for non-2xx responses.

    For compatibility with existing unit tests/mocks: if `status_code` is not
    present, this falls back to `response.raise_for_status()` if available.
    """
    raw_status = getattr(response, "status_code", None)
    try:
        status_code = int(raw_status) if raw_status is not None else None
    except (TypeError, ValueError):
        status_code = None

    if status_code is None:
        # Fall back to requests behavior if we're dealing with a simple mock.
        if hasattr(response, "raise_for_status"):
            response.raise_for_status()
        return

    if 200 <= int(status_code) < 400:
        return

    url = getattr(response, "url", None)
    text, data = _safe_response_payload(response)
    message = "HERE API request failed"

    if status_code in (401, 403):
        raise HereAuthenticationError(message, status_code=status_code, url=url, response_text=text, response_json=data)
    if status_code == 404:
        raise HereNotFoundError(message, status_code=status_code, url=url, response_text=text, response_json=data)
    if status_code == 429:
        raise HereRateLimitError(message, status_code=status_code, url=url, response_text=text, response_json=data)
    if 400 <= status_code < 500:
        raise HereClientError(message, status_code=status_code, url=url, response_text=text, response_json=data)
    if status_code >= 500:
        raise HereServerError(message, status_code=status_code, url=url, response_text=text, response_json=data)

    # Defensive fallback.
    raise HereClientError(message, status_code=status_code, url=url, response_text=text, response_json=data)

