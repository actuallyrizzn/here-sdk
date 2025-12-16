# HERE Traffic SDK for Python

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/yourusername/here-traffic-sdk)

A comprehensive, production-ready Python SDK for accessing HERE Technologies Traffic and Incident APIs. Provides 100% coverage of all documented endpoints with full type hints, comprehensive error handling, and extensive test coverage.

## ✨ Features

- ✅ **100% API Coverage** - All documented endpoints (v7, v6.3, and v3)
- ✅ **Dual Authentication** - API Key and OAuth 2.0 support with automatic token management
- ✅ **Type Hints** - Full type annotations throughout for better IDE support
- ✅ **Response Models** - Structured data models with helper methods
- ✅ **100% Test Coverage** - Comprehensive unit, integration, and e2e tests
- ✅ **Well Documented** - Extensive documentation and examples
- ✅ **Production Ready** - Error handling, retries, and best practices

## 📦 Installation

```bash
pip install -e here_traffic_sdk
```

Or install from requirements:

```bash
cd here_traffic_sdk
pip install -r requirements.txt
```

## 🚀 Quick Start

### Using API Key Authentication

```python
from here_traffic_sdk import HereTrafficClient, LocationReference

# Initialize client with API key
client = HereTrafficClient(api_key="YOUR_API_KEY")

# Get traffic flow data for a circular area (London, 1km radius)
flow_response = client.v7.get_flow_circle(
    latitude=51.50643,
    longitude=-0.12719,
    radius_meters=1000,
    location_referencing=LocationReference.SHAPE
)

# Access flow data
flows = flow_response.flows
free_flow_speeds = flow_response.free_flow_speeds
expected_speeds = flow_response.expected_speeds

print(f"Found {len(flows)} flow segments")
print(f"Average free flow speed: {sum(free_flow_speeds) / len(free_flow_speeds):.1f} km/h")

# Get traffic incidents
incidents_response = client.v7.get_incidents_circle(
    latitude=51.50643,
    longitude=-0.12719,
    radius_meters=1000
)

# Access incident data
incidents = incidents_response.incidents
critical_incidents = incidents_response.get_critical_incidents()

print(f"Found {incidents_response.incident_count} incidents")
print(f"Critical incidents: {len(critical_incidents)}")
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

## 📚 API Coverage

### Traffic API v7 (Current) - ✅ 100% Coverage

- ✅ `GET /flow` - Traffic flow data
- ✅ `GET /incidents` - Traffic incident data  
- ✅ `GET /availability` - API availability information

### Traffic API v6.3 (Legacy) - ✅ 100% Coverage

- ✅ `GET /flow.json` - Traffic flow data
- ✅ `GET /incidents.json` - Traffic incident data

### Traffic API v3 (Legacy) - ✅ 100% Coverage

- ✅ `GET /flow` - Traffic flow data

## 📖 Documentation

- **[SDK Documentation](./here_traffic_sdk/README.md)** - Complete SDK documentation
- **[API Endpoints](./docs/)** - Complete API endpoint documentation
- **[Examples](./here_traffic_sdk/examples/)** - Usage examples
- **[Test Coverage](./here_traffic_sdk/TEST_COVERAGE.md)** - Test coverage report

## 💡 Usage Examples

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
filter_str = GeospatialFilter.circle(51.50643, -0.12719, 2000)
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
    print(f"Coverage areas: {len(availability.coverage_areas)}")
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

## 🧪 Testing

The SDK has **100% test coverage** across unit, integration, and e2e tests.

```bash
cd here_traffic_sdk

# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage report
pytest --cov=here_traffic_sdk --cov-report=html

# Run specific test categories
pytest tests/unit -v          # Unit tests
pytest tests/integration -v  # Integration tests
pytest tests/e2e -v -m e2e   # E2E tests
```

See [TEST_COVERAGE.md](./here_traffic_sdk/TEST_COVERAGE.md) for detailed coverage information.

## 📋 Requirements

- Python 3.8+
- requests >= 2.28.0

## 🔐 Authentication

### Getting API Credentials

1. Sign up at [HERE Platform](https://platform.here.com)
2. Create an application
3. Generate an API Key or OAuth 2.0 credentials

### API Key Authentication

The simplest method. Just provide your API key:

```python
client = HereTrafficClient(api_key="YOUR_API_KEY")
```

### OAuth 2.0 Authentication

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

See [Authentication Guide](./docs/authentication.md) for detailed information.

## 🏗️ Project Structure

```
here-sdk/
├── here_traffic_sdk/          # Python SDK package
│   ├── here_traffic_sdk/      # Main SDK module
│   │   ├── __init__.py        # Package exports
│   │   ├── client.py          # Main client
│   │   ├── auth.py            # Authentication
│   │   ├── v7.py              # API v7 client
│   │   ├── v6.py              # API v6.3 client
│   │   ├── v3.py              # API v3 client
│   │   └── models.py          # Response models
│   ├── tests/                 # Test suite
│   │   ├── unit/              # Unit tests
│   │   ├── integration/       # Integration tests
│   │   └── e2e/               # E2E tests
│   ├── examples/              # Usage examples
│   ├── setup.py               # Package setup
│   ├── requirements.txt       # Dependencies
│   └── README.md              # SDK documentation
├── docs/                      # API documentation
│   ├── all_endpoints.md       # Endpoint reference
│   ├── authentication.md     # Auth guide
│   └── README.md              # Docs index
└── README.md                  # This file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/here-traffic-sdk.git
cd here-traffic-sdk

# Install in development mode
cd here_traffic_sdk
pip install -e .

# Install test dependencies
pip install -r requirements-dev.txt

# Run tests
pytest
```

## 📄 License

**Code License:** [GNU Affero General Public License v3.0](./LICENSE-AGPL-3.0.txt) (AGPL-3.0)

**Documentation License:** [Creative Commons Attribution-ShareAlike 4.0 International](./LICENSE-DOCS) (CC BY-SA 4.0)

- Source code is licensed under AGPL-3.0
- Documentation, README files, and all non-code content is licensed under CC BY-SA 4.0

## 🔗 Resources

- **HERE Developer Portal:** https://developer.here.com
- **Traffic API Documentation:** https://developer.here.com/documentation/traffic
- **Traffic Incidents Guide:** https://developer.here.com/documentation/traffic/dev_guide/topics/traffic-incidents.html
- **Authentication Guide:** https://developer.here.com/documentation/authentication
- **HERE Platform:** https://platform.here.com

## 🐛 Support

For issues and questions:
- Check the [official HERE documentation](https://developer.here.com/documentation/traffic)
- Review the [SDK documentation](./here_traffic_sdk/README.md)
- Check [examples](./here_traffic_sdk/examples/)
- Open an issue on GitHub

## ⚡ Key Features

### Real-time Traffic Data
- Traffic flow data updated every minute
- Traffic incident data updated every two minutes
- Coverage across 70+ countries
- 13+ million kilometers of roads

### Multiple Location Referencing
- **Shape Points** - Coordinate-based location referencing
- **TMC** - Traffic Message Channel standard
- **OLR** - OpenLR Location Referencing

### Flexible Geospatial Filters
- Circle filters (latitude, longitude, radius)
- Bounding box filters
- Corridor/polyline filters

### Response Models
- `TrafficFlowResponse` - Flow data with helper methods
- `TrafficIncidentResponse` - Incident data with filtering
- `AvailabilityResponse` - Availability information

## 📊 Status

- ✅ **100% API Coverage** - All documented endpoints implemented
- ✅ **100% Test Coverage** - Unit, integration, and e2e tests
- ✅ **Production Ready** - Error handling, type hints, documentation
- ✅ **Well Maintained** - Comprehensive documentation and examples

---

**Made with ❤️ for the HERE Technologies community**
