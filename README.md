# HERE Traffic SDK

A comprehensive Python SDK for accessing HERE Technologies Traffic and Incident APIs.

## Features

- ✅ **100% API Coverage** - All documented endpoints (v7 and v6.3)
- ✅ **Dual Authentication** - API Key and OAuth 2.0 support
- ✅ **Type Hints** - Full type annotations for better IDE support
- ✅ **Response Models** - Structured data models for API responses
- ✅ **Easy to Use** - Simple, intuitive API
- ✅ **Well Documented** - Comprehensive documentation and examples

## Quick Start

### Installation

```bash
cd here_traffic_sdk
pip install -e .
```

### Basic Usage

```python
from here_traffic_sdk import HereTrafficClient, LocationReference

# Initialize client
client = HereTrafficClient(api_key="YOUR_API_KEY")

# Get traffic flow data
response = client.v7.get_flow_circle(
    latitude=51.50643,
    longitude=-0.12719,
    radius_meters=1000
)

print(f"Found {len(response.flows)} flow segments")

# Get traffic incidents
incidents = client.v7.get_incidents_circle(
    latitude=51.50643,
    longitude=-0.12719,
    radius_meters=1000
)

print(f"Found {incidents.incident_count} incidents")
```

## Documentation

- **[SDK Documentation](./here_traffic_sdk/README.md)** - Complete SDK documentation
- **[API Endpoints](./docs/)** - Complete API endpoint documentation
- **[Examples](./here_traffic_sdk/examples/)** - Usage examples

## API Coverage

### Traffic API v7 (Current)
- ✅ `GET /flow` - Traffic flow data
- ✅ `GET /incidents` - Traffic incident data
- ✅ `GET /availability` - API availability information

### Traffic API v6.3 (Legacy)
- ✅ `GET /flow.json` - Traffic flow data
- ✅ `GET /incidents.json` - Traffic incident data

## Project Structure

```
here-sdk/
├── here_traffic_sdk/          # Python SDK package
│   ├── here_traffic_sdk/      # Main SDK module
│   │   ├── __init__.py        # Package exports
│   │   ├── client.py          # Main client
│   │   ├── auth.py            # Authentication
│   │   ├── v7.py              # API v7 client
│   │   ├── v6.py              # API v6.3 client
│   │   └── models.py           # Response models
│   ├── examples/              # Usage examples
│   ├── setup.py               # Package setup
│   ├── requirements.txt       # Dependencies
│   └── README.md              # SDK documentation
└── docs/                      # API documentation
    ├── traffic_api_v7_endpoints.md
    ├── traffic_api_v6_endpoints.md
    ├── authentication.md
    └── all_endpoints.md
```

## Requirements

- Python 3.8+
- requests >= 2.28.0

## License

MIT License

## Support

For issues and questions:
- Check the [official HERE documentation](https://developer.here.com/documentation/traffic)
- Review the [SDK documentation](./here_traffic_sdk/README.md)
- Check [examples](./here_traffic_sdk/examples/)
