"""
Security-focused unit tests for input validation.
"""

import math

import pytest

from here_traffic_sdk.models import GeospatialFilter


@pytest.mark.security
def test_corridor_rejects_newlines_and_whitespace():
    for bad in ["abc\n123", "abc\r123", "abc\t123", "abc 123"]:
        with pytest.raises(ValueError):
            GeospatialFilter.corridor(bad)

@pytest.mark.security
def test_corridor_rejects_non_string_and_empty_string():
    with pytest.raises(ValueError):
        GeospatialFilter.corridor(123)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        GeospatialFilter.corridor("")


@pytest.mark.security
def test_circle_rejects_invalid_radius():
    for bad_radius in [0, -1, True, 1.5, "10"]:
        with pytest.raises(ValueError):
            GeospatialFilter.circle(0.0, 0.0, bad_radius)  # type: ignore[arg-type]

@pytest.mark.security
def test_circle_rejects_non_numeric_coordinates():
    with pytest.raises(ValueError):
        GeospatialFilter.circle("0", 0.0, 1)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        GeospatialFilter.circle(0.0, "0", 1)  # type: ignore[arg-type]


@pytest.mark.security
def test_circle_rejects_nan_or_infinite_coordinates():
    for bad in [math.nan, math.inf, -math.inf]:
        with pytest.raises(ValueError):
            GeospatialFilter.circle(bad, 0.0, 1)
        with pytest.raises(ValueError):
            GeospatialFilter.circle(0.0, bad, 1)

