"""
Pytest configuration and shared fixtures
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import json
from here_traffic_sdk.auth import AuthClient, AuthMethod


@pytest.fixture
def mock_api_key():
    """Mock API key for testing"""
    return "test_api_key_12345"


@pytest.fixture
def mock_oauth_credentials():
    """Mock OAuth credentials for testing"""
    return {
        "access_key_id": "test_access_key_id",
        "access_key_secret": "test_access_key_secret"
    }


@pytest.fixture
def mock_oauth_token_response():
    """Mock OAuth token response"""
    return {
        "access_token": "test_access_token_12345",
        "token_type": "Bearer",
        "expires_in": 3600
    }


@pytest.fixture
def auth_client_api_key(mock_api_key):
    """AuthClient with API key authentication"""
    return AuthClient(api_key=mock_api_key, auth_method=AuthMethod.API_KEY)


@pytest.fixture
def auth_client_oauth(mock_oauth_credentials):
    """AuthClient with OAuth authentication"""
    return AuthClient(
        access_key_id=mock_oauth_credentials["access_key_id"],
        access_key_secret=mock_oauth_credentials["access_key_secret"],
        auth_method=AuthMethod.OAUTH
    )


@pytest.fixture
def mock_flow_response():
    """Mock traffic flow API response"""
    return {
        "flows": [
            {
                "freeFlowSpeed": 60.0,
                "expectedSpeed": 45.0,
                "jamFactor": 0.25,
                "location": {
                    "latitude": 51.50643,
                    "longitude": -0.12719
                }
            },
            {
                "freeFlowSpeed": 50.0,
                "expectedSpeed": 30.0,
                "jamFactor": 0.4,
                "location": {
                    "latitude": 51.50743,
                    "longitude": -0.12819
                }
            }
        ]
    }


@pytest.fixture
def mock_incidents_response():
    """Mock traffic incidents API response"""
    return {
        "incidents": [
            {
                "type": "accident",
                "criticality": "critical",
                "startTime": "2024-01-01T10:00:00Z",
                "endTime": "2024-01-01T12:00:00Z",
                "description": "Road closure due to accident",
                "location": {
                    "latitude": 51.50643,
                    "longitude": -0.12719
                }
            },
            {
                "type": "construction",
                "criticality": "minor",
                "startTime": "2024-01-01T08:00:00Z",
                "endTime": "2024-01-01T18:00:00Z",
                "description": "Road works",
                "location": {
                    "latitude": 51.50743,
                    "longitude": -0.12819
                }
            }
        ]
    }


@pytest.fixture
def mock_availability_response():
    """Mock availability API response"""
    return {
        "available": True,
        "coverage": [
            {
                "country": "GB",
                "region": "London"
            }
        ]
    }


@pytest.fixture
def mock_requests_session():
    """Mock requests session"""
    with patch('here_traffic_sdk.v7.requests.Session') as mock_session_class:
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        yield mock_session


@pytest.fixture
def mock_requests_post():
    """Mock requests.post for OAuth"""
    with patch('here_traffic_sdk.auth.requests.post') as mock_post:
        yield mock_post

