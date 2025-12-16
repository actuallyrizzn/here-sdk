"""
Async wrapper for HERE Traffic API v6.3 (legacy).
"""

from __future__ import annotations

from typing import Any

from .async_utils import to_thread
from .models import TrafficFlowResponse, TrafficIncidentResponse
from .v6 import TrafficAPIv6


class AsyncTrafficAPIv6:
    """Async wrapper around :class:`here_traffic_sdk.v6.TrafficAPIv6`."""

    def __init__(self, sync_api: TrafficAPIv6):
        self._sync = sync_api

    async def get_flow(self, bbox: str, **kwargs: Any) -> TrafficFlowResponse:
        return await to_thread(self._sync.get_flow, bbox, **kwargs)

    async def get_flow_bbox(
        self, lat1: float, lon1: float, lat2: float, lon2: float, **kwargs: Any
    ) -> TrafficFlowResponse:
        return await to_thread(self._sync.get_flow_bbox, lat1, lon1, lat2, lon2, **kwargs)

    async def get_incidents(self, bbox: str, **kwargs: Any) -> TrafficIncidentResponse:
        return await to_thread(self._sync.get_incidents, bbox, **kwargs)

    async def get_incidents_bbox(
        self, lat1: float, lon1: float, lat2: float, lon2: float, **kwargs: Any
    ) -> TrafficIncidentResponse:
        return await to_thread(self._sync.get_incidents_bbox, lat1, lon1, lat2, lon2, **kwargs)

    async def aclose(self) -> None:
        await to_thread(self._sync.close)

    async def __aenter__(self) -> "AsyncTrafficAPIv6":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

