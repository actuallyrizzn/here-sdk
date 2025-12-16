"""
Async wrapper for HERE Traffic API v3 (legacy).
"""

from __future__ import annotations

from typing import Any

from .async_utils import to_thread
from .models import TrafficFlowResponse
from .v3 import TrafficAPIv3


class AsyncTrafficAPIv3:
    """Async wrapper around :class:`here_traffic_sdk.v3.TrafficAPIv3`."""

    def __init__(self, sync_api: TrafficAPIv3):
        self._sync = sync_api

    async def get_flow(self, **kwargs: Any) -> TrafficFlowResponse:
        return await to_thread(self._sync.get_flow, **kwargs)

    async def aclose(self) -> None:
        await to_thread(self._sync.close)

    async def __aenter__(self) -> "AsyncTrafficAPIv3":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

