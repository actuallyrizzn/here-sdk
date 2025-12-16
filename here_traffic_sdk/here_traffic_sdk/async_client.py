"""
Async client for HERE Traffic SDK.

This is a non-blocking (async/await) facade around the existing synchronous
client. Under the hood, synchronous I/O is executed in a worker thread.
"""

from __future__ import annotations

from typing import Optional

from .async_utils import to_thread
from .auth import AuthMethod
from .client import HereTrafficClient
from .async_v7 import AsyncTrafficAPIv7
from .async_v6 import AsyncTrafficAPIv6
from .async_v3 import AsyncTrafficAPIv3


class AsyncHereTrafficClient:
    """
    Async variant of :class:`here_traffic_sdk.client.HereTrafficClient`.

    Example:
        >>> client = AsyncHereTrafficClient(api_key="YOUR_API_KEY")
        >>> resp = await client.v7.get_availability()
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        access_key_id: Optional[str] = None,
        access_key_secret: Optional[str] = None,
        auth_method: AuthMethod = AuthMethod.API_KEY,
    ):
        self._sync = HereTrafficClient(
            api_key=api_key,
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            auth_method=auth_method,
        )

        self.v7 = AsyncTrafficAPIv7(self._sync.v7)
        self.v6 = AsyncTrafficAPIv6(self._sync.v6)
        self.v3 = AsyncTrafficAPIv3(self._sync.v3)

    @property
    def auth_client(self):
        """Access the underlying (sync) AuthClient instance."""
        return self._sync.auth_client

    @property
    def flow(self) -> AsyncTrafficAPIv7:
        """Access to traffic flow endpoints (v7)."""
        return self.v7

    @property
    def incidents(self) -> AsyncTrafficAPIv7:
        """Access to traffic incident endpoints (v7)."""
        return self.v7

    @property
    def availability(self) -> AsyncTrafficAPIv7:
        """Access to availability endpoint (v7)."""
        return self.v7

    async def aclose(self) -> None:
        """Close underlying HTTP sessions."""
        await to_thread(self._sync.close)

    async def __aenter__(self) -> "AsyncHereTrafficClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

