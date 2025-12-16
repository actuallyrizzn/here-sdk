"""
Unit tests for shared HTTP utilities.
"""

import logging
from unittest.mock import Mock, MagicMock

import pytest

from here_traffic_sdk.http import HttpConfig, _has_header, _redact_headers, _redact_params, get_json


class TestHttpUtils:
    def test_has_header_case_insensitive(self):
        assert _has_header({"X-Request-Id": "1"}, "x-request-id") is True
        assert _has_header({"x-request-id": "1"}, "X-Request-Id") is True
        assert _has_header({"Other": "1"}, "X-Request-Id") is False

    def test_redact_headers_authorization(self):
        redacted = _redact_headers({"Authorization": "secret", "X": "y"})
        assert redacted["Authorization"] == "<redacted>"
        assert redacted["X"] == "y"

    def test_redact_params_apikey(self):
        redacted = _redact_params({"apiKey": "secret", "bbox": "1,2;3,4"})
        assert redacted["apiKey"] == "<redacted>"
        assert redacted["bbox"] == "1,2;3,4"

    def test_get_json_injects_request_id_and_returns_it(self):
        session = MagicMock()
        response = Mock()
        response.raise_for_status = Mock()
        response.json.return_value = {"ok": True}
        session.get.return_value = response

        cfg = HttpConfig(request_id_factory=lambda: "rid-123")
        payload, rid = get_json(session=session, url="https://example.com", params={}, headers={}, config=cfg)

        assert payload == {"ok": True}
        assert rid == "rid-123"
        assert session.get.call_args[1]["headers"]["X-Request-Id"] == "rid-123"

    def test_get_json_respects_existing_request_id_header(self):
        session = MagicMock()
        response = Mock()
        response.raise_for_status = Mock()
        response.json.return_value = {"ok": True}
        session.get.return_value = response

        cfg = HttpConfig(request_id_factory=lambda: "rid-generated")
        payload, rid = get_json(
            session=session,
            url="https://example.com",
            params={},
            headers={"X-Request-Id": "rid-existing"},
            config=cfg,
        )

        assert payload == {"ok": True}
        assert rid == "rid-existing"
        assert session.get.call_args[1]["headers"]["X-Request-Id"] == "rid-existing"

    def test_get_json_invalid_json_raises_value_error(self):
        session = MagicMock()
        response = Mock()
        response.raise_for_status = Mock()
        response.json.side_effect = ValueError("bad json")
        session.get.return_value = response

        cfg = HttpConfig(request_id_factory=lambda: "rid-err")
        with pytest.raises(ValueError, match="Invalid JSON response"):
            get_json(session=session, url="https://example.com", params={}, headers={}, config=cfg)

    def test_get_json_non_object_payload_raises_value_error(self):
        session = MagicMock()
        response = Mock()
        response.raise_for_status = Mock()
        response.json.return_value = ["not", "a", "dict"]
        session.get.return_value = response

        cfg = HttpConfig(request_id_factory=lambda: "rid-type")
        with pytest.raises(ValueError, match="Unexpected JSON payload type"):
            get_json(session=session, url="https://example.com", params={}, headers={}, config=cfg)

    def test_get_json_logging_redacts_secrets(self, caplog):
        session = MagicMock()
        response = Mock()
        response.raise_for_status = Mock()
        response.json.return_value = {"ok": True}
        response.status_code = 200
        session.get.return_value = response

        logger = logging.getLogger("here_traffic_sdk.http.test")
        cfg = HttpConfig(
            enable_logging=True,
            logger=logger,
            request_id_factory=lambda: "rid-log",
        )

        with caplog.at_level(logging.DEBUG, logger="here_traffic_sdk.http.test"):
            get_json(
                session=session,
                url="https://example.com",
                params={"apiKey": "secret", "bbox": "1,2;3,4"},
                headers={"Authorization": "Bearer secret"},
                config=cfg,
            )

        records = [r for r in caplog.records if r.message == "HERE SDK request"]
        assert len(records) == 1
        rec = records[0]
        assert rec.request_id == "rid-log"
        assert rec.params["apiKey"] == "<redacted>"
        assert rec.headers["Authorization"] == "<redacted>"

