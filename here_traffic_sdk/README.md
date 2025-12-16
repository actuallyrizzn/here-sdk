# HERE Traffic SDK for Python

A comprehensive Python SDK for accessing HERE Traffic and Incident APIs. Supports API v7 (current) and v6.3 (legacy).

## Features

- ✅ **Complete API Coverage** - All documented endpoints (v7 and v6.3)
- ✅ **Dual Authentication** - API Key and OAuth 2.0 support
- ✅ **Type Hints** - Full type annotations for better IDE support
- ✅ **Response Models** - Structured data models for API responses
- ✅ **Easy to Use** - Simple, intuitive API
- ✅ **Well Documented** - Comprehensive documentation and examples

## Installation

```bash
pip install -e .
```

Or install from requirements:

```bash
pip install -r requirements.txt
```

## Quick Start

### Using API Key Authentication

```python
from here_traffic_sdk import HereTrafficClient, LocationReference, GeospatialFilter

# Initialize client with API key
client = HereTrafficClient(api_key="YOUR_API_KEY")

# Get traffic flow data for a circular area (London)
response = client.v7.get_flow_circle(
    latitude=51.50643,
    longitude=-0.12719,
    radius_meters=1000,
    location_referencing=LocationReference.SHAPE
)

# Access flow data
flows = response.flows
free_flow_speeds = response.free_flow_speeds
expected_speeds = response.expected_speeds

# Get traffic incidents
incidents_response = client.v7.get_incidents_circle(
    latitude=51.50643,
    longitude=-0.12719,
    radius_meters=1000
)

# Access incident data
incidents = incidents_response.incidents
critical_incidents = incidents_response.get_critical_incidents()
```

### Using OAuth 2.0 Authentication

```python
from here_traffic_sdk import HereTrafficClient, AuthMethod

# Initialize client with OAuth credentials
client = HereTrafficClient(
    access_key_id="YOUR_ACCESS_KEY_ID",
    access_key_secret="YOUR_ACCESS_KEY_SECRET",
    auth_method=AuthMethod.OAUTH
)

# Use the client the same way
response = client.v7.get_flow_circle(51.50643, -0.12719, 1000)
```

## API Coverage

### Traffic API v7 (Current)

- ✅ `GET /flow` - Traffic flow data
- ✅ `GET /incidents` - Traffic incident data
- ✅ `GET /availability` - API availability information

### Traffic API v6.3 (Legacy)

- ✅ `GET /flow.json` - Traffic flow data
- ✅ `GET /incidents.json` - Traffic incident data

## Usage Examples

### Traffic Flow Data

```python
from here_traffic_sdk import HereTrafficClient, LocationReference, GeospatialFilter

client = HereTrafficClient(api_key="YOUR_API_KEY")

# Using circle filter
response = client.v7.get_flow_circle(
    latitude=51.50643,
    longitude=-0.12719,
    radius_meters=1000
)

# Using bounding box filter
response = client.v7.get_flow_bbox(
    lat1=51.5,
    lon1=-0.13,
    lat2=51.51,
    lon2=-0.12
)

# Using custom geospatial filter
filter_str = GeospatialFilter.circle(51.50643, -0.12719, 1000)
response = client.v7.get_flow(
    location_referencing=LocationReference.SHAPE,
    geospatial_filter=filter_str
)
```

### Traffic Incidents

```python
# Get incidents in a circular area
response = client.v7.get_incidents_circle(
    latitude=51.50643,
    longitude=-0.12719,
    radius_meters=1000
)

# Get all incidents
all_incidents = response.incidents

# Get only critical incidents
critical = response.get_critical_incidents()

# Filter by type
accidents = response.get_incidents_by_type("accident")
```

### API Availability

```python
# Check API availability
availability = client.v7.get_availability()

if availability.available:
    print("API is available")
    print(f"Coverage areas: {availability.coverage_areas}")
```

### Using Legacy v6.3 API

```python
# Use v6.3 API (legacy)
response = client.v6.get_flow_bbox(
    lat1=51.5,
    lon1=-0.13,
    lat2=51.51,
    lon2=-0.12
)
```

## Response Models

The SDK provides structured response models:

- `TrafficFlowResponse` - Traffic flow data with helper methods
- `TrafficIncidentResponse` - Traffic incident data with filtering methods
- `AvailabilityResponse` - API availability information

## Location Referencing

The SDK supports multiple location referencing methods:

- `LocationReference.SHAPE` - Shape points (coordinate-based)
- `LocationReference.TMC` - Traffic Message Channel
- `LocationReference.OLR` - OpenLR Location Referencing

## Geospatial Filters

The SDK provides helper methods for creating geospatial filters:

```python
from here_traffic_sdk import GeospatialFilter

# Circle filter
circle = GeospatialFilter.circle(latitude=51.50643, longitude=-0.12719, radius_meters=1000)

# Bounding box filter
bbox = GeospatialFilter.bbox(lat1=51.5, lon1=-0.13, lat2=51.51, lon2=-0.12)

# Corridor/polyline filter
corridor = GeospatialFilter.corridor(encoded_polyline="encoded_polyline_string")
```

## Error Handling

The SDK uses `requests` library which raises exceptions for HTTP errors:

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

## Authentication

### API Key

The simplest authentication method. Just provide your API key:

```python
client = HereTrafficClient(api_key="YOUR_API_KEY")
```

### OAuth 2.0

For enhanced security, use OAuth 2.0:

```python
from here_traffic_sdk import HereTrafficClient, AuthMethod

client = HereTrafficClient(
    access_key_id="YOUR_ACCESS_KEY_ID",
    access_key_secret="YOUR_ACCESS_KEY_SECRET",
    auth_method=AuthMethod.OAUTH
)
```

The OAuth token is automatically managed and refreshed as needed.

## Requirements

- Python 3.8+
- requests >= 2.28.0

## Documentation

For detailed API documentation, see the `docs/` directory:

- [Traffic API v7 Endpoints](../docs/traffic_api_v7_endpoints.md)
- [Traffic API v6.3 Endpoints](../docs/traffic_api_v6_endpoints.md)
- [Authentication Guide](../docs/authentication.md)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions:
- Check the [official HERE documentation](https://developer.here.com/documentation/traffic)
- Open an issue on GitHub
- Contact HERE Technical Support

