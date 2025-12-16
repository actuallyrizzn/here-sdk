# HERE Traffic SDK - User Guide

Complete user guide for the HERE Traffic SDK.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Authentication](#authentication)
3. [Basic Usage](#basic-usage)
4. [Advanced Usage](#advanced-usage)
5. [Error Handling](#error-handling)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

## Getting Started

### Installation

```bash
pip install -e here_traffic_sdk
```

### First Steps

1. **Get API Credentials**
   - Sign up at [HERE Platform](https://platform.here.com)
   - Create an application
   - Generate an API Key or OAuth credentials

2. **Initialize the Client**
   ```python
   from here_traffic_sdk import HereTrafficClient
   
   client = HereTrafficClient(api_key="YOUR_API_KEY")
   ```

3. **Make Your First Request**
   ```python
   response = client.v7.get_flow_circle(51.50643, -0.12719, 1000)
   print(f"Found {len(response.flows)} flow segments")
   ```

## Authentication

### API Key Authentication

Simplest method for getting started:

```python
client = HereTrafficClient(api_key="YOUR_API_KEY")
```

**Security Tips:**
- Never commit API keys to version control
- Use environment variables: `os.getenv("HERE_API_KEY")`
- Restrict API keys to trusted domains

### OAuth 2.0 Authentication

More secure for production applications:

```python
from here_traffic_sdk import HereTrafficClient, AuthMethod

client = HereTrafficClient(
    access_key_id="YOUR_ACCESS_KEY_ID",
    access_key_secret="YOUR_ACCESS_KEY_SECRET",
    auth_method=AuthMethod.OAUTH
)
```

**Benefits:**
- Automatic token management
- Token refresh handled automatically
- More secure for server-to-server communication

## Basic Usage

### Getting Traffic Flow Data

```python
# Circle area
flow = client.v7.get_flow_circle(
    latitude=51.50643,
    longitude=-0.12719,
    radius_meters=1000
)

# Bounding box
flow = client.v7.get_flow_bbox(
    lat1=51.5,
    lon1=-0.13,
    lat2=51.51,
    lon2=-0.12
)

# Access data
for flow_segment in flow.flows:
    print(f"Free flow: {flow_segment['freeFlowSpeed']} km/h")
    print(f"Expected: {flow_segment['expectedSpeed']} km/h")
```

### Getting Traffic Incidents

```python
# Get incidents
incidents = client.v7.get_incidents_circle(
    latitude=51.50643,
    longitude=-0.12719,
    radius_meters=1000
)

# Filter critical incidents
critical = incidents.get_critical_incidents()

# Filter by type
accidents = incidents.get_incidents_by_type("accident")
```

### Checking API Availability

```python
availability = client.v7.get_availability()

if availability.available:
    print("API is operational")
    print(f"Coverage: {len(availability.coverage_areas)} areas")
```

## Advanced Usage

### Custom Geospatial Filters

```python
from here_traffic_sdk import GeospatialFilter, LocationReference

# Create custom filter
circle = GeospatialFilter.circle(51.50643, -0.12719, 2000)
bbox = GeospatialFilter.bbox(51.5, -0.13, 51.51, -0.12)

# Use with API call
response = client.v7.get_flow(
    location_referencing=LocationReference.SHAPE,
    geospatial_filter=circle
)
```

### Location Referencing Methods

```python
from here_traffic_sdk import LocationReference

# Shape points (coordinate-based)
response = client.v7.get_flow(
    location_referencing=LocationReference.SHAPE,
    geospatial_filter="circle:51.50643,-0.12719;r=1000"
)

# TMC (Traffic Message Channel)
response = client.v7.get_flow(
    location_referencing=LocationReference.TMC,
    geospatial_filter="circle:51.50643,-0.12719;r=1000"
)

# OLR (OpenLR Location Referencing)
response = client.v7.get_flow(
    location_referencing=LocationReference.OLR,
    geospatial_filter="circle:51.50643,-0.12719;r=1000"
)
```

### Additional Parameters

```python
# Pass additional query parameters
response = client.v7.get_flow_circle(
    51.50643, -0.12719, 1000,
    custom_param="value"
)
```

### Using Multiple API Versions

```python
# Use v7 (current)
v7_flow = client.v7.get_flow_circle(51.50643, -0.12719, 1000)

# Use v6.3 (legacy)
v6_flow = client.v6.get_flow_bbox(51.5, -0.13, 51.51, -0.12)

# Use v3 (very old legacy)
v3_flow = client.v3.get_flow()
```

## Error Handling

### Basic Error Handling

```python
import requests
from here_traffic_sdk import HereTrafficClient

client = HereTrafficClient(api_key="YOUR_API_KEY")

try:
    response = client.v7.get_flow_circle(51.50643, -0.12719, 1000)
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        print("Authentication failed - check your API key")
    elif e.response.status_code == 429:
        print("Rate limit exceeded - wait before retrying")
    else:
        print(f"HTTP Error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

### Retry Logic

```python
import time
import requests

def get_flow_with_retry(client, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.v7.get_flow_circle(51.50643, -0.12719, 1000)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                wait_time = 2 ** attempt
                print(f"Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
                continue
            raise
    raise Exception("Max retries exceeded")
```

## Best Practices

### 1. Environment Variables

```python
import os
from here_traffic_sdk import HereTrafficClient

api_key = os.getenv("HERE_API_KEY")
if not api_key:
    raise ValueError("HERE_API_KEY environment variable not set")

client = HereTrafficClient(api_key=api_key)
```

### 2. Reuse Client Instances

```python
# Good: Create once, reuse many times
client = HereTrafficClient(api_key=api_key)

for location in locations:
    flow = client.v7.get_flow_circle(location.lat, location.lon, 1000)
    # Process flow data
```

### 3. Handle Rate Limits

```python
import time

def safe_api_call(func, *args, **kwargs):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                wait = 2 ** attempt
                time.sleep(wait)
                continue
            raise
    raise Exception("Max retries exceeded")
```

### 4. Cache Responses

```python
from functools import lru_cache
import time

@lru_cache(maxsize=100)
def get_cached_flow(client, lat, lon, radius, timestamp):
    # Cache for 1 minute
    return client.v7.get_flow_circle(lat, lon, radius)

# Usage
current_minute = int(time.time() / 60)
flow = get_cached_flow(client, 51.50643, -0.12719, 1000, current_minute)
```

## Troubleshooting

### Common Issues

#### 1. Authentication Errors

**Problem:** `401 Unauthorized`

**Solutions:**
- Verify your API key is correct
- Check that API key hasn't expired
- Ensure API key has proper permissions
- For OAuth, verify credentials are correct

#### 2. Rate Limiting

**Problem:** `429 Too Many Requests`

**Solutions:**
- Implement retry logic with exponential backoff
- Reduce request frequency
- Cache responses when possible
- Check your API plan limits

#### 3. Invalid Parameters

**Problem:** `400 Bad Request`

**Solutions:**
- Verify geospatial filter format
- Check location coordinates are valid
- Ensure required parameters are provided
- Review API documentation for parameter formats

#### 4. Network Issues

**Problem:** Connection timeouts or errors

**Solutions:**
- Check internet connectivity
- Verify HERE API status
- Implement retry logic
- Check firewall/proxy settings

### Debugging

Enable verbose logging:

```python
import logging
import requests

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.DEBUG)
```

## Additional Resources

- [API Reference](./API_REFERENCE.md)
- [Authentication Guide](./authentication.md)
- [Examples](../here_traffic_sdk/examples/)
- [HERE Developer Portal](https://developer.here.com)

