"""
Shared HTTP utilities for HERE Traffic SDK.

Centralizes request configuration:
- timeouts
- SSL verification
- request id correlation
- request/response logging (redacted)
- robust JSON parsing
"""

from __future__ import annotations
from dataclasses import dataclass, field
import logging
import time
import uuid
from typing import Any, Callable, Dict, Mapping, Optional, Sequence, Tuple, Union
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import requests
from .exceptions import raise_for_status_with_context

TimeoutType = Union[float, Tuple[float, float]]
VerifyType = Union[bool, str]


def _default_request_id() -> str:
    return str(uuid.uuid4())


def _has_header(headers: Mapping[str, str], name: str) -> bool:
    target = name.lower()
    return any(k.lower() == target for k in headers.keys())


def _redact_headers(headers: Mapping[str, str]) -> Dict[str, str]:
    redacted: Dict[str, str] = {}
    for k, v in headers.items():
        lk = k.lower()
        if lk == "authorization":
            redacted[k] = "<redacted>"
        else:
            redacted[k] = v
    return redacted


def _redact_params(params: Mapping[str, Any]) -> Dict[str, Any]:
    redacted: Dict[str, Any] = {}
    for k, v in params.items():
        if str(k).lower() in {"apikey", "api_key", "access_token", "token"}:
            redacted[k] = "<redacted>"
        else:
            redacted[k] = v
    return redacted


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


@dataclass(frozen=True)
class HttpConfig:
    """
    HTTP request configuration.

    timeout:
        Passed to requests as `timeout=...`. Use None to disable timeouts (not recommended).
    verify:
        Passed to requests as `verify=...`. Supports bool or CA bundle path.
    enable_logging:
        When True, logs request + response metadata at DEBUG level.
    request_id_factory:
        Called to generate a request id per request. Defaults to uuid4 string.
    logger:
        Logger used when enable_logging is True.
    retry_config:
        Retry configuration for automatic retries on transient errors.
    """

    timeout: Optional[TimeoutType] = 30.0
    verify: VerifyType = True
    enable_logging: bool = False
    request_id_factory: Callable[[], str] = _default_request_id
    logger: logging.Logger = field(default_factory=lambda: logging.getLogger("here_traffic_sdk.http"))
    retry_config: Optional[RetryConfig] = None


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


def get_json(
    *,
    session: requests.Session,
    url: str,
    params: Mapping[str, Any],
    headers: Mapping[str, str],
    config: HttpConfig,
) -> Tuple[Dict[str, Any], str]:
    """
    Perform a GET request and parse a JSON response.

    Returns:
        (parsed_json, request_id)

    Raises:
        requests.RequestException / requests.HTTPError for transport/HTTP errors.
        ValueError for invalid JSON payloads.
    """

    req_headers: Dict[str, str] = dict(headers)
    request_id: Optional[str] = None
    for k, v in req_headers.items():
        if k.lower() == "x-request-id":
            request_id = v
            break
    if request_id is None:
        request_id = config.request_id_factory()
        req_headers["X-Request-Id"] = request_id

    retry_cfg = config.retry_config or RetryConfig()
    retries_remaining = max(0, int(retry_cfg.max_retries))
    attempt = 0
    
    # Use timeout from retry config if available, otherwise from HttpConfig
    timeout_value = retry_cfg.timeout if retry_cfg.timeout else config.timeout

    while True:
        start = time.monotonic()
        try:
            response = session.get(
                url,
                params=dict(params),
                headers=req_headers,
                timeout=timeout_value,
                verify=config.verify,
            )
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            if retries_remaining <= 0:
                raise
            sleep_seconds = min(retry_cfg.max_backoff, retry_cfg.backoff_factor * (2**attempt))
            time.sleep(max(0.0, float(sleep_seconds)))
            retries_remaining -= 1
            attempt += 1
            continue

        elapsed_ms = (time.monotonic() - start) * 1000.0
        if config.enable_logging:
            status_code = getattr(response, "status_code", None)
            config.logger.debug(
                "HERE SDK request",
                extra={
                    "method": "GET",
                    "url": url,
                    "params": _redact_params(params),
                    "headers": _redact_headers(req_headers),
                    "status_code": status_code,
                    "elapsed_ms": round(elapsed_ms, 2),
                    "request_id": request_id,
                    "attempt": attempt + 1,
                },
            )

        status = getattr(response, "status_code", None)
        if status in retry_cfg.retry_statuses and retries_remaining > 0:
            retry_after = None
            if status == 429:
                header_value = None
                try:
                    header_value = response.headers.get("Retry-After")
                except Exception:
                    header_value = None
                if isinstance(header_value, str):
                    retry_after = _retry_after_seconds(header_value)

            sleep_seconds = retry_after
            if sleep_seconds is None:
                sleep_seconds = min(retry_cfg.max_backoff, retry_cfg.backoff_factor * (2**attempt))

            time.sleep(max(0.0, float(sleep_seconds)))
            retries_remaining -= 1
            attempt += 1
            continue

        raise_for_status_with_context(
            response=response,
            method="GET",
            url=url,
            prefix="HERE_TRAFFIC_SDK_HTTP_ERROR",
        )
        try:
            payload = response.json()
        except ValueError as e:
            raise ValueError(f"Invalid JSON response (request_id={request_id}, url={url})") from e

        if not isinstance(payload, dict):
            # The SDK models expect JSON objects at the top level.
            raise ValueError(
                f"Unexpected JSON payload type: {type(payload).__name__} (request_id={request_id}, url={url})"
            )

        return payload, request_id

