"""
HTTP retry helpers (rate limiting / transient errors).

Internal module: not part of the public API.

Note: RetryConfig is defined in http.py to avoid circular imports.
This module provides get_with_retries() for standalone retry logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import time
from typing import Mapping, Optional, Sequence

import requests


# Duplicate RetryConfig definition to avoid circular import with http.py
# This matches the definition in http.py exactly
@dataclass(frozen=True)
class RetryConfig:
    """
    Configuration for retry/backoff behavior.

    max_retries:
        Number of retries after the initial request. Set to 0 to disable retries.
    """

    max_retries: int = 3
    timeout: float = 30.0
    backoff_factor: float = 0.5
    max_backoff: float = 8.0
    retry_statuses: Sequence[int] = (429, 500, 502, 503, 504)


def _retry_after_seconds(retry_after_value: str) -> Optional[float]:
    """
    Parse Retry-After header value.

    Supports delta-seconds and HTTP-date as per RFC 7231.
    Returns None if parsing fails.
    """

    value = retry_after_value.strip()
    if not value:
        return None

    # delta-seconds
    if value.isdigit():
        return float(value)

    # HTTP-date
    try:
        dt = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None

    # Ensure aware datetime
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    seconds = (dt - now).total_seconds()
    return max(0.0, seconds)


def get_with_retries(
    session: requests.Session,
    url: str,
    *,
    params: Optional[Mapping[str, object]] = None,
    headers: Optional[Mapping[str, str]] = None,
    retry_config: Optional[RetryConfig] = None,
) -> requests.Response:
    """
    Perform a GET request with basic retry/backoff behavior.

    Retries on:
    - HTTP 429 (rate limited), respecting Retry-After where present
    - Transient 5xx statuses (configurable)
    - requests timeouts / connection errors
    """

    cfg = retry_config or RetryConfig()
    retries_remaining = max(0, int(cfg.max_retries))

    attempt = 0
    while True:
        try:
            response = session.get(
                url,
                params=params,
                headers=headers,
                timeout=cfg.timeout,
            )
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            if retries_remaining <= 0:
                raise
            sleep_seconds = min(cfg.max_backoff, cfg.backoff_factor * (2**attempt))
            time.sleep(max(0.0, float(sleep_seconds)))
            retries_remaining -= 1
            attempt += 1
            continue

        status = getattr(response, "status_code", None)
        if status in cfg.retry_statuses and retries_remaining > 0:
            retry_after = None
            if status == 429:
                header_value = None
                try:
                    header_value = response.headers.get("Retry-After")  # type: ignore[union-attr]
                except Exception:
                    header_value = None
                if isinstance(header_value, str):
                    retry_after = _retry_after_seconds(header_value)

            sleep_seconds = retry_after
            if sleep_seconds is None:
                sleep_seconds = min(cfg.max_backoff, cfg.backoff_factor * (2**attempt))

            time.sleep(max(0.0, float(sleep_seconds)))
            retries_remaining -= 1
            attempt += 1
            continue

        response.raise_for_status()
        return response

