"""
HERE Traffic API SDK for Python

A comprehensive Python SDK for accessing HERE Traffic and Incident APIs.
Supports API v7 (current) and v6.3 (legacy).

Copyright (C) 2024 HERE Traffic SDK Contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
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

from ._version import __version__
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

