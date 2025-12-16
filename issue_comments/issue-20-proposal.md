## Investigation
The SDK uses `response.raise_for_status()` directly. This yields generic `requests.HTTPError` exceptions with limited context and no categorization (auth vs rate limit vs server error).

## Proposed fix
- Introduce SDK exception types (e.g. `HereAPIError`, `HereAuthenticationError`, `HereRateLimitError`, `HereServerError`, etc.).
- Centralize response handling in a helper (e.g. `_raise_for_here_status(response)`), mapping common status codes:
  - 401/403 -> auth error
  - 429 -> rate limit error
  - 4xx -> client error
  - 5xx -> server error
- Include response metadata (status code, URL, best-effort parsed JSON/text) in exception messages/fields.

## Test plan
- Add unit tests that mock responses with specific status codes and assert the SDK raises the correct custom exception.
