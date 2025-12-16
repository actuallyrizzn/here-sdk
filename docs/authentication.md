# HERE API Authentication Guide

**Source:** https://developer.here.com/documentation/authentication

---

## Overview

HERE APIs support multiple authentication methods to secure API access. This guide covers the available authentication options for the Traffic and Incident APIs.

---

## Authentication Methods

### 1. API Key Authentication

API Key authentication is the simplest method for authenticating API requests.

#### Setup

1. Sign up or log in to the [HERE Platform](https://platform.here.com)
2. Navigate to the "Access Manager" or "Access location services" section
3. Click on "Create an app" or "Create an application"
4. Enter a name for your application and register it
5. Generate an API key for your application

#### Usage

Include the API key as a query parameter in your API requests:

```
?apiKey=YOUR_API_KEY
```

**Example:**
```bash
curl "https://data.traffic.hereapi.com/v7/flow?locationReferencing=shape&in=circle:51.50643,-0.12719;r=1000&apiKey=YOUR_API_KEY"
```

#### Security Best Practices

- **Never expose API keys in client-side code**
- **Restrict API key usage to specific domains** (Trusted Domains feature)
- **Rotate API keys regularly**
- **Use environment variables** to store API keys
- **Monitor API key usage** for unauthorized access

#### Trusted Domains Configuration

To add an extra layer of security:

1. In the "Access Manager," select your app
2. Enable "Trusted domains"
3. Specify the domains allowed to use your API key

This restricts API key usage to specified domains, preventing unauthorized access.

---

### 2. OAuth 2.0 Authentication

OAuth 2.0 provides enhanced security for server-to-server interactions.

#### Setup

1. Sign up or log in to the [HERE Platform](https://platform.here.com)
2. Navigate to the "Access Manager"
3. Create an application (if not already created)
4. Generate OAuth 2.0 credentials:
   - **Access Key ID**
   - **Access Key Secret**
5. **Important:** Download and securely store the Access Key Secret immediately, as it cannot be retrieved later

#### Obtaining an Access Token

Use your OAuth credentials to obtain an access token. The exact endpoint and process may vary - refer to the official OAuth documentation.

**Example token request:**
```bash
curl -X POST "https://account.api.here.com/oauth2/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=YOUR_ACCESS_KEY_ID" \
  -d "client_secret=YOUR_ACCESS_KEY_SECRET"
```

#### Usage

Include the OAuth token in the `Authorization` header:

```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Example:**
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "https://data.traffic.hereapi.com/v7/flow?locationReferencing=shape&in=circle:51.50643,-0.12719;r=1000"
```

#### Security Best Practices

- **Store credentials securely** (use secure credential storage)
- **Never commit credentials to version control**
- **Use token refresh mechanisms** when tokens expire
- **Rotate credentials periodically**
- **Monitor token usage** for anomalies

---

### 3. JWT Authentication

Some HERE APIs may support JWT (JSON Web Token) authentication. Refer to specific API documentation for JWT support.

---

## Authentication Endpoints

### OAuth Token Endpoint

**Endpoint:** `POST /oauth2/token`

**Base URL:** `https://account.api.here.com/oauth2/token`

**Content-Type:** `application/x-www-form-urlencoded`

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `grant_type` | string | Yes | Must be `client_credentials` |
| `client_id` | string | Yes | Your Access Key ID |
| `client_secret` | string | Yes | Your Access Key Secret |

**Response:**

```json
{
  "access_token": "YOUR_ACCESS_TOKEN",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

---

## Error Responses

### Authentication Errors

| HTTP Status Code | Description |
|-----------------|-------------|
| 401 | Unauthorized - Invalid or missing authentication credentials |
| 403 | Forbidden - Access denied, credentials may be valid but lack required permissions |

### Common Error Scenarios

1. **Missing API Key:**
   - Error: 401 Unauthorized
   - Solution: Include `apiKey` parameter in request

2. **Invalid API Key:**
   - Error: 401 Unauthorized
   - Solution: Verify API key is correct and active

3. **Expired OAuth Token:**
   - Error: 401 Unauthorized
   - Solution: Refresh the OAuth token

4. **Invalid OAuth Credentials:**
   - Error: 401 Unauthorized
   - Solution: Verify Access Key ID and Secret are correct

---

## Implementation Examples

### Python Example (API Key)

```python
import requests

api_key = "YOUR_API_KEY"
url = "https://data.traffic.hereapi.com/v7/flow"
params = {
    "locationReferencing": "shape",
    "in": "circle:51.50643,-0.12719;r=1000",
    "apiKey": api_key
}

response = requests.get(url, params=params)
data = response.json()
```

### Python Example (OAuth)

```python
import requests

# Get access token
token_url = "https://account.api.here.com/oauth2/token"
token_data = {
    "grant_type": "client_credentials",
    "client_id": "YOUR_ACCESS_KEY_ID",
    "client_secret": "YOUR_ACCESS_KEY_SECRET"
}
token_response = requests.post(token_url, data=token_data)
access_token = token_response.json()["access_token"]

# Make API request
api_url = "https://data.traffic.hereapi.com/v7/flow"
headers = {"Authorization": f"Bearer {access_token}"}
params = {
    "locationReferencing": "shape",
    "in": "circle:51.50643,-0.12719;r=1000"
}

response = requests.get(api_url, headers=headers, params=params)
data = response.json()
```

### JavaScript Example (API Key)

```javascript
const apiKey = 'YOUR_API_KEY';
const url = `https://data.traffic.hereapi.com/v7/flow?locationReferencing=shape&in=circle:51.50643,-0.12719;r=1000&apiKey=${apiKey}`;

fetch(url)
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

### JavaScript Example (OAuth)

```javascript
// Get access token
const tokenUrl = 'https://account.api.here.com/oauth2/token';
const tokenData = new URLSearchParams({
  grant_type: 'client_credentials',
  client_id: 'YOUR_ACCESS_KEY_ID',
  client_secret: 'YOUR_ACCESS_KEY_SECRET'
});

fetch(tokenUrl, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded'
  },
  body: tokenData
})
  .then(response => response.json())
  .then(tokenResponse => {
    const accessToken = tokenResponse.access_token;
    
    // Make API request
    const apiUrl = 'https://data.traffic.hereapi.com/v7/flow?locationReferencing=shape&in=circle:51.50643,-0.12719;r=1000';
    return fetch(apiUrl, {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    });
  })
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

---

## Additional Resources

- **HERE Platform:** https://platform.here.com
- **Authentication Blog Post:** https://www.here.com/learn/blog/authentication-on-here-platform
- **OAuth Tutorial Video:** https://www.youtube.com/watch?v=HzpPMlDbdJ0
- **Trusted Domains Guide:** https://www.here.com/learn/blog/trusted-domains-here-platform

---

## Security Recommendations

1. **Never commit credentials to version control**
2. **Use environment variables or secure credential stores**
3. **Implement credential rotation policies**
4. **Monitor API usage for anomalies**
5. **Use HTTPS for all API requests**
6. **Implement rate limiting on your side**
7. **Log authentication failures for security monitoring**
8. **Use OAuth 2.0 for server-to-server communications**
9. **Restrict API keys to trusted domains when possible**
10. **Regularly review and audit API access**
