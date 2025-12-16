"""
HERE Traffic API SDK for Python

A comprehensive Python SDK for accessing HERE Traffic and Incident APIs.
Supports API v7 (current) and v6.3 (legacy).
"""

from .client import HereTrafficClient
from .auth import AuthClient, AuthMethod
from .v7 import TrafficAPIv7
from .v6 import TrafficAPIv6
from .v3 import TrafficAPIv3
from .models import (
    TrafficFlowResponse,
    TrafficIncidentResponse,
    AvailabilityResponse,
    LocationReference,
    GeospatialFilter,
)

__version__ = "1.0.0"
__all__ = [
    "HereTrafficClient",
    "AuthClient",
    "AuthMethod",
    "TrafficAPIv7",
    "TrafficAPIv6",
    "TrafficAPIv3",
    "TrafficFlowResponse",
    "TrafficIncidentResponse",
    "AvailabilityResponse",
    "LocationReference",
    "GeospatialFilter",
]

