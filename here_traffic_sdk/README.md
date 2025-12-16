# HERE Traffic SDK - Detailed Documentation

Complete documentation for the HERE Traffic SDK Python package.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Authentication](#authentication)
- [API Reference](#api-reference)
- [Response Models](#response-models)
- [Examples](#examples)
- [Error Handling](#error-handling)
- [Testing](#testing)

## Installation

```bash
pip install -e .
```

Or from requirements:

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from here_traffic_sdk import HereTrafficClient, LocationReference

# Initialize with API key
client = HereTrafficClient(api_key="YOUR_API_KEY")

# Get traffic flow
flow = client.v7.get_flow_circle(51.50643, -0.12719, 1000)
print(f"Found {len(flow.flows)} flow segments")

# Get incidents
incidents = client.v7.get_incidents_circle(51.50643, -0.12719, 1000)
print(f"Found {incidents.incident_count} incidents")
```

## Authentication

### API Key

```python
client = HereTrafficClient(api_key="YOUR_API_KEY")
```

### OAuth 2.0

```python
from here_traffic_sdk import HereTrafficClient, AuthMethod

client = HereTrafficClient(
    access_key_id="YOUR_ACCESS_KEY_ID",
    access_key_secret="YOUR_ACCESS_KEY_SECRET",
    auth_method=AuthMethod.OAUTH
)
```

## API Reference

### Traffic API v7

#### Get Flow Data

```python
# Circle filter
response = client.v7.get_flow_circle(lat, lon, radius_meters)

# Bounding box filter
response = client.v7.get_flow_bbox(lat1, lon1, lat2, lon2)

# Custom filter
response = client.v7.get_flow(
    location_referencing=LocationReference.SHAPE,
    geospatial_filter="circle:51.50643,-0.12719;r=1000"
)
```

#### Get Incidents

```python
# Circle filter
response = client.v7.get_incidents_circle(lat, lon, radius_meters)

# Bounding box filter
response = client.v7.get_incidents_bbox(lat1, lon1, lat2, lon2)

# Custom filter
response = client.v7.get_incidents(
    location_referencing=LocationReference.SHAPE,
    geospatial_filter="circle:51.50643,-0.12719;r=1000"
)
```

#### Get Availability

```python
availability = client.v7.get_availability()
if availability.available:
    print("API is available")
```

### Traffic API v6.3 (Legacy)

```python
# Flow data
response = client.v6.get_flow_bbox(lat1, lon1, lat2, lon2)

# Incidents
response = client.v6.get_incidents_bbox(lat1, lon1, lat2, lon2)
```

### Traffic API v3 (Legacy)

```python
response = client.v3.get_flow()
```

## Response Models

### TrafficFlowResponse

```python
response = client.v7.get_flow_circle(51.50643, -0.12719, 1000)

# Access flows
flows = response.flows

# Get speeds
free_flow_speeds = response.free_flow_speeds
expected_speeds = response.expected_speeds

# Raw response
raw_data = response.raw_response
```

### TrafficIncidentResponse

```python
response = client.v7.get_incidents_circle(51.50643, -0.12719, 1000)

# Access incidents
incidents = response.incidents
count = response.incident_count

# Filter methods
critical = response.get_critical_incidents()
accidents = response.get_incidents_by_type("accident")
```

### AvailabilityResponse

```python
availability = client.v7.get_availability()

# Check availability
is_available = availability.available

# Get coverage
coverage = availability.coverage_areas
```

## Examples

See the [examples directory](./examples/) for complete usage examples.

## Error Handling

The SDK uses `requests` library exceptions:

```python
import requests
from here_traffic_sdk import HereTrafficClient

client = HereTrafficClient(api_key="YOUR_API_KEY")

try:
    response = client.v7.get_flow_circle(51.50643, -0.12719, 1000)
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request Error: {e}")
```

## Testing

See [TEST_COVERAGE.md](./TEST_COVERAGE.md) for detailed test coverage information.

## License

Code: AGPL-3.0  
Documentation: CC BY-SA 4.0
