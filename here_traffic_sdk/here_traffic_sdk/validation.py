"""
Input validation and sanitization helpers.

These utilities are used by:
- GeospatialFilter helpers (circle/bbox/corridor)
- API client methods that accept user-provided coordinates / kwargs
"""

from __future__ import annotations

import re
from typing import Any, Dict, Mapping, Union


_BBOX_RE = re.compile(
    r"^\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*;\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*$"
)


def validate_latitude(lat: Any) -> float:
    try:
        value = float(lat)
    except (TypeError, ValueError):
        raise ValueError(f"Latitude must be a number, got {lat!r}")
    if not (-90.0 <= value <= 90.0):
        raise ValueError(f"Latitude must be between -90 and 90, got {value}")
    return value


def validate_longitude(lon: Any) -> float:
    try:
        value = float(lon)
    except (TypeError, ValueError):
        raise ValueError(f"Longitude must be a number, got {lon!r}")
    if not (-180.0 <= value <= 180.0):
        raise ValueError(f"Longitude must be between -180 and 180, got {value}")
    return value


def validate_radius_meters(radius_meters: Any, *, max_radius_meters: int = 100_000) -> int:
    try:
        value = int(radius_meters)
    except (TypeError, ValueError):
        raise ValueError(f"Radius must be an integer number of meters, got {radius_meters!r}")
    if value < 0:
        raise ValueError(f"Radius must be non-negative, got {value}")
    if value > max_radius_meters:
        raise ValueError(f"Radius too large (max {max_radius_meters}m), got {value}")
    return value


def validate_encoded_polyline(encoded_polyline: Any) -> str:
    if not isinstance(encoded_polyline, str):
        raise ValueError(f"Encoded polyline must be a string, got {type(encoded_polyline).__name__}")
    # Reject control characters and grammar delimiters even if they're only in surrounding whitespace.
    if any(ch in encoded_polyline for ch in [";", "\n", "\r", "\t"]):
        raise ValueError("Encoded polyline contains invalid characters")
    value = encoded_polyline.strip()
    if not value:
        raise ValueError("Encoded polyline must be non-empty")
    return value


def validate_geospatial_filter(filter_str: Any) -> str:
    """
    Validate a HERE v7 `in=` filter string.

    This is intentionally conservative: it ensures the value is a string,
    non-empty, and doesn't contain control characters that can confuse the API's
    filter grammar. It does *not* attempt to fully parse/validate all filter
    variants.
    """
    if not isinstance(filter_str, str):
        raise ValueError(f"geospatial_filter must be a string, got {type(filter_str).__name__}")
    if any(ch in filter_str for ch in ["\n", "\r", "\t"]):
        raise ValueError("geospatial_filter contains invalid characters")
    value = filter_str.strip()
    if not value:
        raise ValueError("geospatial_filter must be non-empty")
    return value


def validate_bbox_string(bbox: Any) -> str:
    if not isinstance(bbox, str):
        raise ValueError(f"bbox must be a string, got {type(bbox).__name__}")
    match = _BBOX_RE.match(bbox)
    if not match:
        raise ValueError('bbox must be in format "LAT1,LON1;LAT2,LON2"')
    lat1, lon1, lat2, lon2 = (float(match.group(i)) for i in range(1, 5))
    validate_latitude(lat1)
    validate_longitude(lon1)
    validate_latitude(lat2)
    validate_longitude(lon2)
    # Normalize formatting for consistent requests.
    return f"{lat1},{lon1};{lat2},{lon2}"


Primitive = Union[str, int, float, bool]


def _is_primitive(value: Any) -> bool:
    return value is None or isinstance(value, (str, int, float, bool))


def sanitize_query_params(params: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Ensure query params are safe to hand to `requests`.

    - keys must be strings
    - values must be primitives or list/tuple of primitives
    - `None` values are omitted
    """
    clean: Dict[str, Any] = {}
    for key, value in params.items():
        if not isinstance(key, str):
            raise ValueError(f"Query parameter keys must be strings, got {type(key).__name__}")
        if value is None:
            continue
        if _is_primitive(value):
            clean[key] = value
            continue
        if isinstance(value, (list, tuple)):
            if not all(_is_primitive(v) for v in value):
                raise ValueError(f"Query parameter {key!r} must be primitives, got {value!r}")
            clean[key] = value
            continue
        raise ValueError(f"Query parameter {key!r} must be a primitive or list of primitives, got {type(value).__name__}")
    return clean

