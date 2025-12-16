"""
Async wrapper for HERE Traffic API v7.

This provides an awaitable API surface while reusing the existing synchronous
implementation under the hood (executed in a worker thread).
"""

from __future__ import annotations

from typing import Any

from .async_utils import to_thread
from .models import AvailabilityResponse, LocationReference, TrafficFlowResponse, TrafficIncidentResponse
from .v7 import TrafficAPIv7


class AsyncTrafficAPIv7:
    """Async wrapper around :class:`here_traffic_sdk.v7.TrafficAPIv7`."""

    def __init__(self, sync_api: TrafficAPIv7):
        self._sync = sync_api

    async def get_flow(
        self,
        location_referencing: LocationReference,
        geospatial_filter: str,
        **kwargs: Any,
    ) -> TrafficFlowResponse:
        return await to_thread(self._sync.get_flow, location_referencing, geospatial_filter, **kwargs)

    async def get_flow_circle(
        self,
        latitude: float,
        longitude: float,
        radius_meters: int,
        location_referencing: LocationReference = LocationReference.SHAPE,
        **kwargs: Any,
    ) -> TrafficFlowResponse:
        return await to_thread(
            self._sync.get_flow_circle,
            latitude,
            longitude,
            radius_meters,
            location_referencing,
            **kwargs,
        )

    async def get_flow_bbox(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
        location_referencing: LocationReference = LocationReference.SHAPE,
        **kwargs: Any,
    ) -> TrafficFlowResponse:
        return await to_thread(
            self._sync.get_flow_bbox,
            lat1,
            lon1,
            lat2,
            lon2,
            location_referencing,
            **kwargs,
        )

    async def get_incidents(
        self,
        location_referencing: LocationReference,
        geospatial_filter: str,
        **kwargs: Any,
    ) -> TrafficIncidentResponse:
        return await to_thread(self._sync.get_incidents, location_referencing, geospatial_filter, **kwargs)

    async def get_incidents_circle(
        self,
        latitude: float,
        longitude: float,
        radius_meters: int,
        location_referencing: LocationReference = LocationReference.SHAPE,
        **kwargs: Any,
    ) -> TrafficIncidentResponse:
        return await to_thread(
            self._sync.get_incidents_circle,
            latitude,
            longitude,
            radius_meters,
            location_referencing,
            **kwargs,
        )

    async def get_incidents_bbox(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
        location_referencing: LocationReference = LocationReference.SHAPE,
        **kwargs: Any,
    ) -> TrafficIncidentResponse:
        return await to_thread(
            self._sync.get_incidents_bbox,
            lat1,
            lon1,
            lat2,
            lon2,
            location_referencing,
            **kwargs,
        )

    async def get_availability(self, **kwargs: Any) -> AvailabilityResponse:
        return await to_thread(self._sync.get_availability, **kwargs)

    async def aclose(self) -> None:
        await to_thread(self._sync.close)

    async def __aenter__(self) -> "AsyncTrafficAPIv7":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

