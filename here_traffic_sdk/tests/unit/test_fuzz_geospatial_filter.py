"""
Property-based tests ("fuzzing") for geospatial filters.
"""

import pytest
from hypothesis import given, settings, strategies as st

from here_traffic_sdk.models import GeospatialFilter


latitudes = st.floats(min_value=-90.0, max_value=90.0, allow_nan=False, allow_infinity=False, width=32)
longitudes = st.floats(min_value=-180.0, max_value=180.0, allow_nan=False, allow_infinity=False, width=32)
radii = st.integers(min_value=1, max_value=100000)


@pytest.mark.fuzz
@settings(max_examples=75)
@given(latitude=latitudes, longitude=longitudes, radius=radii)
def test_circle_filter_never_crashes(latitude, longitude, radius):
    s = GeospatialFilter.circle(latitude, longitude, radius)
    assert s.startswith("circle:")
    assert ";r=" in s


@pytest.mark.fuzz
@settings(max_examples=75)
@given(lat1=latitudes, lon1=longitudes, lat2=latitudes, lon2=longitudes)
def test_bbox_filter_never_crashes(lat1, lon1, lat2, lon2):
    s = GeospatialFilter.bbox(lat1, lon1, lat2, lon2)
    assert s.startswith("bbox:")
    assert ";" in s


safe_polyline = st.text(
    alphabet=st.sampled_from(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-~.")),
    min_size=1,
    max_size=200,
)


@pytest.mark.fuzz
@settings(max_examples=75)
@given(polyline=safe_polyline)
def test_corridor_filter_never_crashes(polyline):
    s = GeospatialFilter.corridor(polyline)
    assert s == f"corridor:{polyline}"


invalid_latitudes = st.floats(min_value=-1e6, max_value=1e6, allow_nan=False, allow_infinity=False).filter(
    lambda x: x < -90.0 or x > 90.0
)
invalid_longitudes = st.floats(min_value=-1e6, max_value=1e6, allow_nan=False, allow_infinity=False).filter(
    lambda x: x < -180.0 or x > 180.0
)


@pytest.mark.fuzz
@settings(max_examples=50)
@given(latitude=invalid_latitudes, longitude=longitudes, radius=radii)
def test_circle_rejects_invalid_latitude(latitude, longitude, radius):
    with pytest.raises(ValueError):
        GeospatialFilter.circle(latitude, longitude, radius)


@pytest.mark.fuzz
@settings(max_examples=50)
@given(latitude=latitudes, longitude=invalid_longitudes, radius=radii)
def test_circle_rejects_invalid_longitude(latitude, longitude, radius):
    with pytest.raises(ValueError):
        GeospatialFilter.circle(latitude, longitude, radius)

