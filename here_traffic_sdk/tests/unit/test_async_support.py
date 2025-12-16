import asyncio
from unittest.mock import MagicMock

from here_traffic_sdk.async_client import AsyncHereTrafficClient
from here_traffic_sdk.async_utils import to_thread
from here_traffic_sdk.async_v3 import AsyncTrafficAPIv3
from here_traffic_sdk.async_v6 import AsyncTrafficAPIv6
from here_traffic_sdk.async_v7 import AsyncTrafficAPIv7
from here_traffic_sdk.client import HereTrafficClient
from here_traffic_sdk.models import LocationReference, TrafficFlowResponse


def test_async_v7_delegates_to_sync_method(mock_flow_response):
    sync_api = MagicMock()
    expected = TrafficFlowResponse(data=mock_flow_response, raw_response=mock_flow_response)
    sync_api.get_flow.return_value = expected

    async_api = AsyncTrafficAPIv7(sync_api)

    result = asyncio.run(
        async_api.get_flow(LocationReference.SHAPE, "circle:1,2;r=3", units="metric")
    )

    assert result is expected
    sync_api.get_flow.assert_called_once_with(
        LocationReference.SHAPE, "circle:1,2;r=3", units="metric"
    )


def test_async_v7_other_methods_delegate():
    sync_api = MagicMock()
    sync_api.get_flow_circle.return_value = "flow_circle"
    sync_api.get_flow_bbox.return_value = "flow_bbox"
    sync_api.get_incidents.return_value = "incidents"
    sync_api.get_incidents_circle.return_value = "incidents_circle"
    sync_api.get_incidents_bbox.return_value = "incidents_bbox"
    sync_api.get_availability.return_value = "availability"
    sync_api.close.return_value = None

    async_api = AsyncTrafficAPIv7(sync_api)

    assert (
        asyncio.run(async_api.get_flow_circle(1.0, 2.0, 3, LocationReference.SHAPE, foo="bar"))
        == "flow_circle"
    )
    assert (
        asyncio.run(async_api.get_flow_bbox(1.0, 2.0, 3.0, 4.0, LocationReference.SHAPE, foo="bar"))
        == "flow_bbox"
    )
    assert (
        asyncio.run(async_api.get_incidents(LocationReference.SHAPE, "bbox:1,2;3,4", foo="bar"))
        == "incidents"
    )
    assert (
        asyncio.run(async_api.get_incidents_circle(1.0, 2.0, 3, LocationReference.SHAPE, foo="bar"))
        == "incidents_circle"
    )
    assert (
        asyncio.run(async_api.get_incidents_bbox(1.0, 2.0, 3.0, 4.0, LocationReference.SHAPE, foo="bar"))
        == "incidents_bbox"
    )
    assert asyncio.run(async_api.get_availability(foo="bar")) == "availability"
    asyncio.run(async_api.aclose())
    sync_api.close.assert_called_once()


def test_async_v6_and_v3_delegate():
    sync_v6 = MagicMock()
    sync_v6.get_flow.return_value = "v6_flow"
    sync_v6.get_flow_bbox.return_value = "v6_flow_bbox"
    sync_v6.get_incidents.return_value = "v6_incidents"
    sync_v6.get_incidents_bbox.return_value = "v6_incidents_bbox"
    sync_v6.close.return_value = None

    async_v6 = AsyncTrafficAPIv6(sync_v6)
    assert asyncio.run(async_v6.get_flow("1,2;3,4", foo="bar")) == "v6_flow"
    assert asyncio.run(async_v6.get_flow_bbox(1, 2, 3, 4, foo="bar")) == "v6_flow_bbox"
    assert asyncio.run(async_v6.get_incidents("1,2;3,4", foo="bar")) == "v6_incidents"
    assert asyncio.run(async_v6.get_incidents_bbox(1, 2, 3, 4, foo="bar")) == "v6_incidents_bbox"
    asyncio.run(async_v6.aclose())
    sync_v6.close.assert_called_once()

    sync_v3 = MagicMock()
    sync_v3.get_flow.return_value = "v3_flow"
    sync_v3.close.return_value = None

    async_v3 = AsyncTrafficAPIv3(sync_v3)
    assert asyncio.run(async_v3.get_flow(foo="bar")) == "v3_flow"
    asyncio.run(async_v3.aclose())
    sync_v3.close.assert_called_once()


def test_to_thread_fallback_path(monkeypatch):
    # Force the Python 3.8-compatible fallback branch.
    monkeypatch.delattr(asyncio, "to_thread", raising=False)
    assert asyncio.run(to_thread(lambda x: x + 1, 1)) == 2


def test_async_client_exposes_v7_and_convenience_properties(mock_api_key):
    client = AsyncHereTrafficClient(api_key=mock_api_key)
    try:
        assert client.flow is client.v7
        assert client.incidents is client.v7
        assert client.availability is client.v7
        assert client.auth_client is client._sync.auth_client
    finally:
        asyncio.run(client.aclose())


def test_async_client_aclose_delegates_to_sync_close(mock_api_key):
    client = AsyncHereTrafficClient(api_key=mock_api_key)
    try:
        client._sync.close = MagicMock()
        asyncio.run(client.aclose())
        client._sync.close.assert_called_once()
    finally:
        # In case the mock prevented closing on the first call
        client._sync.close = MagicMock()
        asyncio.run(client.aclose())


def test_async_client_context_manager_calls_aclose(mock_api_key):
    async def _run():
        async with AsyncHereTrafficClient(api_key=mock_api_key) as client:
            assert client.flow is client.v7

    asyncio.run(_run())


def test_async_api_wrappers_support_async_with():
    async def _run():
        sync_v7 = MagicMock()
        sync_v7.close.return_value = None
        async with AsyncTrafficAPIv7(sync_v7) as api_v7:
            assert api_v7 is not None
        sync_v7.close.assert_called_once()

        sync_v6 = MagicMock()
        sync_v6.close.return_value = None
        async with AsyncTrafficAPIv6(sync_v6) as api_v6:
            assert api_v6 is not None
        sync_v6.close.assert_called_once()

        sync_v3 = MagicMock()
        sync_v3.close.return_value = None
        async with AsyncTrafficAPIv3(sync_v3) as api_v3:
            assert api_v3 is not None
        sync_v3.close.assert_called_once()

    asyncio.run(_run())


def test_sync_client_context_manager_calls_close(mock_api_key):
    client = HereTrafficClient(api_key=mock_api_key)
    client.close = MagicMock()

    with client as c:
        assert c is client

    client.close.assert_called_once()

