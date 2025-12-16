"""
Unit tests for config / http / validation helpers.

These tests exist primarily to ensure new infrastructure code is fully covered
and behaves consistently.
"""

import pytest
from unittest.mock import Mock
import requests

from here_traffic_sdk.config import HereTrafficConfig
from here_traffic_sdk import config as config_module
from here_traffic_sdk.exceptions import (
    HereAPIError,
    HereAuthenticationError,
    HereClientError,
    HereConnectionError,
    HereNotFoundError,
    HereRateLimitError,
    HereServerError,
)
from here_traffic_sdk.http import raise_for_here_status
from here_traffic_sdk.validation import (
    sanitize_query_params,
    validate_bbox_string,
    validate_encoded_polyline,
    validate_geospatial_filter,
)
from here_traffic_sdk.v7 import TrafficAPIv7
from here_traffic_sdk.models import LocationReference
from here_traffic_sdk.validation import validate_latitude, validate_longitude, validate_radius_meters
from here_traffic_sdk.v6 import TrafficAPIv6
from here_traffic_sdk.v3 import TrafficAPIv3

def test_config_from_env_defaults(monkeypatch):
    """Config should use defaults when env vars are absent."""
    monkeypatch.delenv("HERE_TRAFFIC_V7_BASE_URL", raising=False)
    monkeypatch.delenv("HERE_HTTP_TIMEOUT_SECONDS", raising=False)
    cfg = HereTrafficConfig.from_env()
    assert cfg.v7_base_url == HereTrafficConfig.v7_base_url
    assert cfg.http_timeout_seconds == 30.0


def test_config_from_env_overrides(monkeypatch):
    """Config should honor environment overrides."""
    monkeypatch.setenv("HERE_TRAFFIC_V7_BASE_URL", "https://example.test/v7")
    monkeypatch.setenv("HERE_HTTP_TIMEOUT_SECONDS", "5")
    cfg = HereTrafficConfig.from_env()
    assert cfg.v7_base_url == "https://example.test/v7"
    assert cfg.http_timeout_seconds == 5.0


def test_config_from_env_invalid_timeout(monkeypatch):
    """Invalid timeout env var should raise a helpful ValueError."""
    monkeypatch.setenv("HERE_HTTP_TIMEOUT_SECONDS", "not-a-number")
    with pytest.raises(ValueError, match="must be a number"):
        HereTrafficConfig.from_env()


def test_config_from_env_ignores_empty_overrides(monkeypatch):
    """Empty/whitespace env vars should be treated as unset."""
    monkeypatch.setenv("HERE_TRAFFIC_V7_BASE_URL", "   ")
    cfg = HereTrafficConfig.from_env()
    assert cfg.v7_base_url == HereTrafficConfig.v7_base_url


def test_here_api_error_string_includes_context():
    """HereAPIError.__str__ should include status/url context when present."""
    err = HereAPIError("boom", status_code=400, url="https://example.test")
    s = str(err)
    assert "boom" in s
    assert "status=400" in s
    assert "url=https://example.test" in s


def test_here_api_error_string_without_context_is_just_message():
    err = HereAPIError("boom")
    assert str(err) == "boom"


def test_internal_get_env_float_returns_none_when_unset(monkeypatch):
    monkeypatch.delenv("SOME_TIMEOUT_VAR", raising=False)
    assert config_module._get_env_float("SOME_TIMEOUT_VAR") is None


def test_raise_for_here_status_fallback_calls_raise_for_status():
    """If status_code is missing, fall back to response.raise_for_status()."""
    resp = Mock()
    resp.raise_for_status = Mock()
    raise_for_here_status(resp)
    resp.raise_for_status.assert_called_once()


def test_raise_for_here_status_fallback_no_raise_for_status_is_noop():
    """If status_code and raise_for_status are missing, do nothing."""
    class Minimal:
        pass

    raise_for_here_status(Minimal())


@pytest.mark.parametrize(
    ("status", "exc_type"),
    [
        (401, HereAuthenticationError),
        (403, HereAuthenticationError),
        (404, HereNotFoundError),
        (429, HereRateLimitError),
        (400, HereClientError),
        (500, HereServerError),
    ],
)
def test_raise_for_here_status_maps_status_codes(status, exc_type):
    """HTTP status codes should map to SDK exception types."""
    resp = Mock()
    resp.status_code = status
    resp.url = "https://example.test"
    resp.text = "oops"
    resp.json.return_value = {"error": "x"}
    with pytest.raises(exc_type):
        raise_for_here_status(resp)


def test_raise_for_here_status_allows_success():
    """2xx responses should not raise."""
    resp = Mock()
    resp.status_code = 200
    raise_for_here_status(resp)


def test_raise_for_here_status_handles_unexpected_status_codes():
    """Statuses outside 2xx/4xx/5xx buckets should still raise a client error."""
    resp = Mock()
    resp.status_code = 100
    resp.url = "https://example.test"
    resp.json.side_effect = RuntimeError("bad json")

    with pytest.raises(HereClientError):
        raise_for_here_status(resp)


def test_raise_for_here_status_handles_bad_payload_access():
    """If response.text/json raise, we should still raise an SDK exception."""
    class BadResponse:
        status_code = 400
        url = "https://example.test"

        @property
        def text(self):
            raise RuntimeError("boom")

        def json(self):
            raise RuntimeError("boom")

    with pytest.raises(HereClientError):
        raise_for_here_status(BadResponse())


def test_safe_response_payload_handles_json_attr_getter_error():
    """If getattr(response, 'json') raises, we should still raise a client error."""
    class JsonAttrRaises:
        status_code = 400
        url = "https://example.test"
        text = "oops"

        @property
        def json(self):
            raise RuntimeError("boom")

    with pytest.raises(HereClientError):
        raise_for_here_status(JsonAttrRaises())


def test_validation_sanitize_query_params_happy_path():
    """sanitize_query_params should keep primitives and omit Nones."""
    clean = sanitize_query_params({"a": 1, "b": "x", "c": None, "d": [1, "y", True]})
    assert clean == {"a": 1, "b": "x", "d": [1, "y", True]}


def test_validation_sanitize_query_params_rejects_bad_key():
    with pytest.raises(ValueError, match="keys must be strings"):
        sanitize_query_params({1: "x"})  # type: ignore[arg-type]


def test_validation_sanitize_query_params_rejects_bad_value():
    with pytest.raises(ValueError, match="must be a primitive"):
        sanitize_query_params({"a": {"nested": "dict"}})


def test_validation_sanitize_query_params_rejects_bad_list_value():
    with pytest.raises(ValueError, match="must be primitives"):
        sanitize_query_params({"a": [1, {"bad": "x"}]})


def test_validate_bbox_string_normalizes_and_validates():
    assert validate_bbox_string(" 51.5,-0.13; 51.51,-0.12 ") == "51.5,-0.13;51.51,-0.12"


def test_validate_bbox_string_rejects_invalid_format():
    with pytest.raises(ValueError, match="bbox must be in format"):
        validate_bbox_string("not-a-bbox")


def test_validate_bbox_string_rejects_non_string():
    with pytest.raises(ValueError, match="bbox must be a string"):
        validate_bbox_string(123)  # type: ignore[arg-type]


def test_validate_geospatial_filter_rejects_control_chars():
    with pytest.raises(ValueError, match="invalid characters"):
        validate_geospatial_filter("circle:0,0;r=1\n")


def test_validate_geospatial_filter_rejects_non_str_and_empty():
    with pytest.raises(ValueError, match="must be a string"):
        validate_geospatial_filter(123)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="non-empty"):
        validate_geospatial_filter("   ")


def test_validate_encoded_polyline_rejects_empty_and_non_str():
    with pytest.raises(ValueError, match="must be a string"):
        validate_encoded_polyline(123)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="non-empty"):
        validate_encoded_polyline("   ")


def test_validate_encoded_polyline_rejects_injection_chars():
    with pytest.raises(ValueError, match="invalid characters"):
        validate_encoded_polyline("abc;def")


def test_validate_latitude_rejects_non_numeric():
    with pytest.raises(ValueError, match="must be a number"):
        validate_latitude("nope")


def test_validate_radius_meters_rejects_too_large():
    with pytest.raises(ValueError, match="Radius too large"):
        validate_radius_meters(100_001, max_radius_meters=100_000)


def test_validate_longitude_rejects_non_numeric_and_out_of_range():
    with pytest.raises(ValueError, match="Longitude must be a number"):
        validate_longitude("nope")
    with pytest.raises(ValueError, match="between -180 and 180"):
        validate_longitude(200)


def test_validate_radius_meters_rejects_non_integer():
    with pytest.raises(ValueError, match="must be an integer"):
        validate_radius_meters("nope")  # type: ignore[arg-type]


def test_v7_connection_errors_are_wrapped(auth_client_api_key, mock_requests_session):
    """Transport errors should raise HereConnectionError."""
    mock_requests_session.get.side_effect = requests.Timeout("boom")
    client = TrafficAPIv7(auth_client_api_key)
    with pytest.raises(HereConnectionError):
        client.get_flow(location_referencing=LocationReference.SHAPE, geospatial_filter="circle:0,0;r=0")


def test_auth_token_connection_errors_are_wrapped(auth_client_oauth, mock_requests_post):
    """OAuth token transport errors should raise HereConnectionError."""
    mock_requests_post.side_effect = requests.Timeout("boom")
    with pytest.raises(HereConnectionError):
        auth_client_oauth._get_oauth_token()


def test_v7_incidents_connection_errors_are_wrapped(auth_client_api_key, mock_requests_session):
    mock_requests_session.get.side_effect = requests.Timeout("boom")
    client = TrafficAPIv7(auth_client_api_key)
    with pytest.raises(HereConnectionError):
        client.get_incidents(location_referencing=LocationReference.SHAPE, geospatial_filter="circle:0,0;r=0")


def test_v7_availability_connection_errors_are_wrapped(auth_client_api_key, mock_requests_session):
    mock_requests_session.get.side_effect = requests.Timeout("boom")
    client = TrafficAPIv7(auth_client_api_key)
    with pytest.raises(HereConnectionError):
        client.get_availability()


def test_v6_connection_errors_are_wrapped(auth_client_api_key, mock_requests_session):
    mock_requests_session.get.side_effect = requests.Timeout("boom")
    client = TrafficAPIv6(auth_client_api_key)
    with pytest.raises(HereConnectionError):
        client.get_flow("0,0;0,0")


def test_v6_incidents_connection_errors_are_wrapped(auth_client_api_key, mock_requests_session):
    mock_requests_session.get.side_effect = requests.Timeout("boom")
    client = TrafficAPIv6(auth_client_api_key)
    with pytest.raises(HereConnectionError):
        client.get_incidents("0,0;0,0")


def test_v3_connection_errors_are_wrapped(auth_client_api_key, mock_requests_session):
    mock_requests_session.get.side_effect = requests.Timeout("boom")
    client = TrafficAPIv3(auth_client_api_key)
    with pytest.raises(HereConnectionError):
        client.get_flow()

