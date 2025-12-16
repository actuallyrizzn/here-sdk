# HERE Traffic API - Complete API Reference

Complete reference documentation for all HERE Traffic and Incident API endpoints.

## Base URLs

- **v7 (Current):** `https://data.traffic.hereapi.com/v7/`
- **v6.3 (Legacy):** `https://traffic.api.here.com/traffic/6.3/`
- **v3 (Legacy):** `https://traffic.api.here.com/v3/`

## Authentication

All endpoints support two authentication methods:

1. **API Key** - Include as query parameter: `?apiKey=YOUR_API_KEY`
2. **OAuth 2.0** - Include in header: `Authorization: Bearer YOUR_TOKEN`

See [Authentication Guide](./authentication.md) for detailed setup instructions.

## API v7 Endpoints

### GET /flow

Get real-time traffic flow data.

**Endpoint:** `https://data.traffic.hereapi.com/v7/flow`

**Method:** `GET`

**Required Parameters:**
- `locationReferencing` (string) - Location referencing method: `shape`, `tmc`, or `olr`
- `in` (string) - Geospatial filter (circle, bbox, or corridor)
- `apiKey` (string) - API key (if using API key auth)

**Example Request:**
```bash
curl "https://data.traffic.hereapi.com/v7/flow?locationReferencing=shape&in=circle:51.50643,-0.12719;r=1000&apiKey=YOUR_API_KEY"
```

**Response:**
```json
{
  "flows": [
    {
      "freeFlowSpeed": 60.0,
      "expectedSpeed": 45.0,
      "jamFactor": 0.25,
      "location": {
        "latitude": 51.50643,
        "longitude": -0.12719
      }
    }
  ]
}
```

### GET /incidents

Get traffic incident data.

**Endpoint:** `https://data.traffic.hereapi.com/v7/incidents`

**Method:** `GET`

**Required Parameters:**
- `locationReferencing` (string) - Location referencing method: `shape`, `tmc`, or `olr`
- `in` (string) - Geospatial filter (circle, bbox, or corridor)
- `apiKey` (string) - API key (if using API key auth)

**Example Request:**
```bash
curl "https://data.traffic.hereapi.com/v7/incidents?locationReferencing=shape&in=circle:51.50643,-0.12719;r=1000&apiKey=YOUR_API_KEY"
```

**Response:**
```json
{
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
    }
  ]
}
```

### GET /availability

Get API availability information.

**Endpoint:** `https://data.traffic.hereapi.com/v7/availability`

**Method:** `GET`

**Required Parameters:**
- `apiKey` (string) - API key (if using API key auth)

**Example Request:**
```bash
curl "https://data.traffic.hereapi.com/v7/availability?apiKey=YOUR_API_KEY"
```

## API v6.3 Endpoints (Legacy)

### GET /flow.json

**Endpoint:** `https://traffic.api.here.com/traffic/6.3/flow.json`

**Method:** `GET`

**Required Parameters:**
- `bbox` (string) - Bounding box: `LAT1,LON1;LAT2,LON2`
- `apiKey` (string) - API key (if using API key auth)

### GET /incidents.json

**Endpoint:** `https://traffic.api.here.com/traffic/6.3/incidents.json`

**Method:** `GET`

**Required Parameters:**
- `bbox` (string) - Bounding box: `LAT1,LON1;LAT2,LON2`
- `apiKey` (string) - API key (if using API key auth)

## API v3 Endpoints (Legacy)

### GET /flow

**Endpoint:** `https://traffic.api.here.com/v3/flow`

**Method:** `GET`

**Note:** This is a very old version. Use v7 for new implementations.

## Geospatial Filters

### Circle Filter
Format: `circle:LATITUDE,LONGITUDE;r=RADIUS_IN_METERS`

Example: `circle:51.50643,-0.12719;r=1000`

### Bounding Box Filter
Format: `bbox:LAT1,LON1;LAT2,LON2`

Example: `bbox:51.5,-0.13;51.51,-0.12`

### Corridor/Polyline Filter
Format: `corridor:ENCODED_POLYLINE`

## Location Referencing

- **shape** - Shape points (coordinate-based)
- **tmc** - Traffic Message Channel
- **olr** - OpenLR Location Referencing

## Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 429 | Too Many Requests |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

## Rate Limits

Rate limits may apply. Refer to your HERE Platform account for specific limits.

## Additional Resources

- [HERE Developer Portal](https://developer.here.com)
- [Traffic API Documentation](https://developer.here.com/documentation/traffic)
- [Authentication Guide](./authentication.md)

