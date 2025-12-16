"""
Centralized SDK constants.

Keeping these in one place avoids duplicated "magic strings" spread across the
codebase and makes future updates safer.
"""

from __future__ import annotations

from ._version import __version__

# Package identification
SDK_NAME = "here-traffic-sdk-python"
DEFAULT_USER_AGENT = f"{SDK_NAME}/{__version__}"

# API base URLs
BASE_URL_V7 = "https://data.traffic.hereapi.com/v7"
BASE_URL_V6 = "https://traffic.api.here.com/traffic/6.3"
BASE_URL_V3 = "https://traffic.api.here.com/v3"

# Auth endpoints
OAUTH_TOKEN_URL = "https://account.api.here.com/oauth2/token"

# HTTP header values
CONTENT_TYPE_FORM_URLENCODED = "application/x-www-form-urlencoded"

