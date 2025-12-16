"""
Unit tests for retry/backoff helpers.
"""

from unittest.mock import MagicMock, Mock, patch

import pytest
import requests

from here_traffic_sdk._retry import RetryConfig, _retry_after_seconds, get_with_retries


class TestRetryAfterParsing:
    def test_retry_after_delta_seconds(self):
        assert _retry_after_seconds("5") == 5.0

    def test_retry_after_empty(self):
        assert _retry_after_seconds("   ") is None

    def test_retry_after_http_date_in_past(self):
        # Fixed past date should clamp to 0.0 seconds.
        assert _retry_after_seconds("Wed, 21 Oct 2015 07:28:00 GMT") == 0.0

    def test_retry_after_http_date_without_tz(self):
        # Date without explicit timezone may parse to naive dt; should still be handled.
        assert _retry_after_seconds("Wed, 21 Oct 2015 07:28:00") == 0.0

    def test_retry_after_invalid(self):
        assert _retry_after_seconds("not-a-date") is None


class TestGetWithRetries:
    def test_retries_on_429_then_succeeds(self):
        session = MagicMock(spec=requests.Session)

        resp_429 = Mock()
        resp_429.status_code = 429
        resp_429.headers = {"Retry-After": "0"}
        resp_429.raise_for_status = Mock()

        resp_200 = Mock()
        resp_200.status_code = 200
        resp_200.headers = {}
        resp_200.raise_for_status = Mock()

        session.get.side_effect = [resp_429, resp_200]

        cfg = RetryConfig(max_retries=1, backoff_factor=0.01, max_backoff=0.01, timeout=1.0)

        with patch("here_traffic_sdk._retry.time.sleep") as sleep:
            result = get_with_retries(
                session,
                "https://example.com/resource",
                params={"a": "b"},
                headers={"h": "v"},
                retry_config=cfg,
            )

        assert result is resp_200
        assert session.get.call_count == 2
        sleep.assert_called_once()

    def test_retries_exhausted_raises_http_error(self):
        session = MagicMock(spec=requests.Session)

        resp_429 = Mock()
        resp_429.status_code = 429
        resp_429.headers = {"Retry-After": "0"}
        resp_429.raise_for_status = Mock(side_effect=requests.HTTPError("429 Too Many Requests"))

        session.get.side_effect = [resp_429, resp_429, resp_429]

        cfg = RetryConfig(max_retries=2, backoff_factor=0.0, max_backoff=0.0, timeout=1.0)

        with patch("here_traffic_sdk._retry.time.sleep"):
            with pytest.raises(requests.HTTPError):
                get_with_retries(session, "https://example.com/resource", retry_config=cfg)

        assert session.get.call_count == 3

    def test_retries_on_timeout_then_succeeds(self):
        session = MagicMock(spec=requests.Session)

        resp_200 = Mock()
        resp_200.status_code = 200
        resp_200.headers = {}
        resp_200.raise_for_status = Mock()

        session.get.side_effect = [
            requests.exceptions.Timeout("timeout"),
            resp_200,
        ]

        cfg = RetryConfig(max_retries=1, backoff_factor=0.0, max_backoff=0.0, timeout=1.0)

        with patch("here_traffic_sdk._retry.time.sleep") as sleep:
            result = get_with_retries(session, "https://example.com/resource", retry_config=cfg)

        assert result is resp_200
        assert session.get.call_count == 2
        sleep.assert_called_once()

    def test_timeout_with_no_retries_raises(self):
        session = MagicMock(spec=requests.Session)
        session.get.side_effect = requests.exceptions.Timeout("timeout")

        cfg = RetryConfig(max_retries=0, backoff_factor=0.0, max_backoff=0.0, timeout=0.01)

        with pytest.raises(requests.exceptions.Timeout):
            get_with_retries(session, "https://example.com/resource", retry_config=cfg)

        assert session.get.call_count == 1

    def test_retries_on_503_uses_exponential_backoff(self):
        session = MagicMock(spec=requests.Session)

        resp_503 = Mock()
        resp_503.status_code = 503
        resp_503.headers = {}
        resp_503.raise_for_status = Mock()

        resp_200 = Mock()
        resp_200.status_code = 200
        resp_200.headers = {}
        resp_200.raise_for_status = Mock()

        session.get.side_effect = [resp_503, resp_200]

        cfg = RetryConfig(max_retries=1, backoff_factor=0.01, max_backoff=0.01, timeout=1.0)

        with patch("here_traffic_sdk._retry.time.sleep") as sleep:
            result = get_with_retries(session, "https://example.com/resource", retry_config=cfg)

        assert result is resp_200
        assert session.get.call_count == 2
        sleep.assert_called_once()

    def test_retry_after_header_access_error_falls_back_to_backoff(self):
        session = MagicMock(spec=requests.Session)

        resp_429 = Mock()
        resp_429.status_code = 429
        resp_429.headers = Mock()
        resp_429.headers.get.side_effect = Exception("boom")
        resp_429.raise_for_status = Mock()

        resp_200 = Mock()
        resp_200.status_code = 200
        resp_200.headers = {}
        resp_200.raise_for_status = Mock()

        session.get.side_effect = [resp_429, resp_200]

        cfg = RetryConfig(max_retries=1, backoff_factor=0.01, max_backoff=0.01, timeout=1.0)

        with patch("here_traffic_sdk._retry.time.sleep") as sleep:
            result = get_with_retries(session, "https://example.com/resource", retry_config=cfg)

        assert result is resp_200
        assert session.get.call_count == 2
        sleep.assert_called_once()

