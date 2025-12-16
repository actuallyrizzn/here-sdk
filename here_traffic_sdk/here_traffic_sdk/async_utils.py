"""
Async helpers for providing non-blocking wrappers around sync implementations.

We support Python 3.8+, so we can't rely solely on asyncio.to_thread (3.9+).
"""

from __future__ import annotations

import asyncio
from functools import partial
from typing import Any, Callable, TypeVar

T = TypeVar("T")


async def to_thread(func: Callable[..., T], /, *args: Any, **kwargs: Any) -> T:
    """
    Run a sync callable in a thread, returning its result asynchronously.

    Uses asyncio.to_thread when available (Python 3.9+), otherwise falls back to
    loop.run_in_executor for Python 3.8 compatibility.
    """

    if hasattr(asyncio, "to_thread"):
        # mypy: asyncio.to_thread exists at runtime on 3.9+
        return await asyncio.to_thread(func, *args, **kwargs)  # type: ignore[attr-defined]

    loop = asyncio.get_running_loop()
    bound = partial(func, *args, **kwargs)
    return await loop.run_in_executor(None, bound)

