"""
Microbenchmarks for common SDK operations.

These benchmarks are intended to catch accidental performance regressions.
They do not enforce hard time thresholds by default.
"""

import pytest

from here_traffic_sdk.models import GeospatialFilter, TrafficFlowResponse


@pytest.mark.performance
def test_benchmark_geospatial_filter_circle(benchmark):
    benchmark(GeospatialFilter.circle, 51.50643, -0.12719, 1000)


@pytest.mark.performance
def test_benchmark_geospatial_filter_bbox(benchmark):
    benchmark(GeospatialFilter.bbox, 51.5, -0.13, 51.51, -0.12)


@pytest.mark.performance
def test_benchmark_geospatial_filter_corridor(benchmark):
    benchmark(GeospatialFilter.corridor, "abcDEF0123_-~.")


@pytest.mark.performance
def test_benchmark_flow_response_speed_access(benchmark):
    data = {
        "flows": [
            {"freeFlowSpeed": 60.0, "expectedSpeed": 45.0} for _ in range(5000)
        ]
    }
    response = TrafficFlowResponse(data=data)

    def access():
        # Access both properties to cover typical usage.
        _ = response.free_flow_speeds
        _ = response.expected_speeds

    benchmark(access)

