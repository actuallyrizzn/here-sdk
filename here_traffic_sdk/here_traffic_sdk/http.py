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
from typing import Any, Callable, Dict, Mapping, Optional, Tuple, Union

import requests

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
    """

    timeout: Optional[TimeoutType] = 30.0
    verify: VerifyType = True
    enable_logging: bool = False
    request_id_factory: Callable[[], str] = _default_request_id
    logger: logging.Logger = field(default_factory=lambda: logging.getLogger("here_traffic_sdk.http"))


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

    start = time.monotonic()
    response = session.get(
        url,
        params=dict(params),
        headers=req_headers,
        timeout=config.timeout,
        verify=config.verify,
    )

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
            },
        )

    response.raise_for_status()
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

