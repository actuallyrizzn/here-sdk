"""
Configuration management for HERE Traffic SDK.

This module provides a small configuration object to allow:
- environment-based overrides (useful for CI/tests)
- custom base URLs for mocking/staging
- centralized HTTP timeout configuration
"""

from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional


def _get_env(name: str) -> Optional[str]:
    value = os.getenv(name)
    if value is None:
        return None
    value = value.strip()
    return value or None


def _get_env_float(name: str) -> Optional[float]:
    raw = _get_env(name)
    if raw is None:
        return None
    try:
        return float(raw)
    except ValueError:
        raise ValueError(f"Environment variable {name} must be a number, got {raw!r}")


@dataclass(frozen=True)
class HereTrafficConfig:
    """SDK runtime configuration."""

    # Base URL overrides (None means "use the SDK default")
    v7_base_url: Optional[str] = None
    v6_base_url: Optional[str] = None
    v3_base_url: Optional[str] = None

    # OAuth token endpoint override (None means "use the SDK default")
    oauth_token_url: Optional[str] = None

    # Requests timeout in seconds (None means requests default)
    http_timeout_seconds: Optional[float] = 30.0

    @classmethod
    def from_env(cls) -> "HereTrafficConfig":
        """
        Create a config from environment variables.

        Supported variables:
        - HERE_TRAFFIC_V7_BASE_URL
        - HERE_TRAFFIC_V6_BASE_URL
        - HERE_TRAFFIC_V3_BASE_URL
        - HERE_OAUTH_TOKEN_URL
        - HERE_HTTP_TIMEOUT_SECONDS
        """
        return cls(
            v7_base_url=_get_env("HERE_TRAFFIC_V7_BASE_URL"),
            v6_base_url=_get_env("HERE_TRAFFIC_V6_BASE_URL"),
            v3_base_url=_get_env("HERE_TRAFFIC_V3_BASE_URL"),
            oauth_token_url=_get_env("HERE_OAUTH_TOKEN_URL"),
            http_timeout_seconds=_get_env_float("HERE_HTTP_TIMEOUT_SECONDS")
            if _get_env("HERE_HTTP_TIMEOUT_SECONDS") is not None
            else cls.http_timeout_seconds,
        )

