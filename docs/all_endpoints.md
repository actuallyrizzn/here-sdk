# HERE Traffic & Incident API - Complete Endpoint Reference

This document provides a comprehensive list of all HERE Traffic and Incident API endpoints.

---

## API v7 Endpoints

**Base URL:** `https://data.traffic.hereapi.com/v7/`

### Traffic Flow

**Endpoint:** `GET /flow`

**Full URL:** `https://data.traffic.hereapi.com/v7/flow`

**Description:** Real-time traffic flow data including speed and congestion levels

**Required Parameters:**
- `locationReferencing` (shape, tmc, olr)
- `in` (geospatial filter: circle, bbox, corridor)
- `apiKey` (if using API key auth)

**Example:**
```
https://data.traffic.hereapi.com/v7/flow?locationReferencing=shape&in=circle:51.50643,-0.12719;r=1000&apiKey=YOUR_API_KEY
```

---

### Traffic Incidents

**Endpoint:** `GET /incidents`

**Full URL:** `https://data.traffic.hereapi.com/v7/incidents`

**Description:** Traffic incident data including accidents, construction, road closures

**Required Parameters:**
- `locationReferencing` (shape, tmc, olr)
- `in` (geospatial filter: circle, bbox, corridor)
- `apiKey` (if using API key auth)

**Example:**
```
https://data.traffic.hereapi.com/v7/incidents?locationReferencing=shape&in=circle:51.50643,-0.12719;r=1000&apiKey=YOUR_API_KEY
```

---

### Availability

**Endpoint:** `GET /availability`

**Full URL:** `https://data.traffic.hereapi.com/v7/availability`

**Description:** API availability and coverage area information

**Required Parameters:**
- `apiKey` (if using API key auth)

**Example:**
```
https://data.traffic.hereapi.com/v7/availability?apiKey=YOUR_API_KEY
```

---

## API v6.3 Endpoints (Legacy)

**Base URL:** `https://traffic.api.here.com/traffic/6.3/`

### Traffic Flow (v6.3)

**Endpoint:** `GET /flow.json`

**Full URL:** `https://traffic.api.here.com/traffic/6.3/flow.json`

**Description:** Legacy traffic flow endpoint

**Required Parameters:**
- `bbox` (bounding box: LAT1,LON1;LAT2,LON2)
- `apiKey` (if using API key auth)

**Example:**
```
https://traffic.api.here.com/traffic/6.3/flow.json?bbox=51.5,-0.13;51.51,-0.12&apiKey=YOUR_API_KEY
```

---

### Traffic Incidents (v6.3)

**Endpoint:** `GET /incidents.json`

**Full URL:** `https://traffic.api.here.com/traffic/6.3/incidents.json`

**Description:** Legacy traffic incidents endpoint

**Required Parameters:**
- `bbox` (bounding box: LAT1,LON1;LAT2,LON2)
- `apiKey` (if using API key auth)

**Example:**
```
https://traffic.api.here.com/traffic/6.3/incidents.json?bbox=51.5,-0.13;51.51,-0.12&apiKey=YOUR_API_KEY
```

---

## API v3 Endpoints (Legacy)

**Base URL:** `https://traffic.api.here.com/v3/`

### Traffic Flow (v3)

**Endpoint:** `GET /flow`

**Full URL:** `https://traffic.api.here.com/v3/flow`

**Description:** Legacy v3 traffic flow endpoint

**Note:** This is an older version. Use v7 for new implementations.

---

## Authentication Endpoints

### OAuth Token Endpoint

**Endpoint:** `POST /oauth2/token`

**Full URL:** `https://account.api.here.com/oauth2/token`

**Description:** Obtain OAuth 2.0 access token

**Content-Type:** `application/x-www-form-urlencoded`

**Required Parameters:**
- `grant_type` (must be `client_credentials`)
- `client_id` (Access Key ID)
- `client_secret` (Access Key Secret)

**Example:**
```bash
curl -X POST "https://account.api.here.com/oauth2/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=YOUR_ACCESS_KEY_ID" \
  -d "client_secret=YOUR_ACCESS_KEY_SECRET"
```

---

## Summary

### Total Endpoints Documented: 6

**v7 Endpoints:** 3
- `/flow`
- `/incidents`
- `/availability`

**v6.3 Endpoints:** 2
- `/flow.json`
- `/incidents.json`

**v3 Endpoints:** 1
- `/flow`

**Authentication Endpoints:** 1
- `/oauth2/token`

---

## Notes

- All endpoints support both API Key and OAuth 2.0 authentication
- v7 is the recommended version for new implementations
- v6.3 and v3 are maintained for backward compatibility
- Response formats may vary between versions
- Refer to individual endpoint documentation for detailed parameter and response information

---

## Quick Reference

| Version | Base URL | Endpoints |
|---------|----------|-----------|
| v7 | `https://data.traffic.hereapi.com/v7/` | `/flow`, `/incidents`, `/availability` |
| v6.3 | `https://traffic.api.here.com/traffic/6.3/` | `/flow.json`, `/incidents.json` |
| v3 | `https://traffic.api.here.com/v3/` | `/flow` |

---

For detailed information about each endpoint, refer to:
- [Traffic API v7 Endpoints](./traffic_api_v7_endpoints.md)
- [Traffic API v6.3 Endpoints](./traffic_api_v6_endpoints.md)
- [Authentication Guide](./authentication.md)
