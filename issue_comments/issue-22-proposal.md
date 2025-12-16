## Investigation
Base URLs and token URL are hardcoded as class constants, making it hard to:
- test against mocks
- use staging/alternate endpoints
- change timeouts/retry behavior

## Proposed fix
- Add a `HereTrafficConfig` object that stores base URLs, token URL, and request timeout.
- Allow construction from environment variables (e.g. `HERE_TRAFFIC_V7_BASE_URL`, `HERE_OAUTH_TOKEN_URL`, `HERE_HTTP_TIMEOUT_SECONDS`).
- Thread the config through `HereTrafficClient` -> `AuthClient` and API version clients.

## Test plan
- Add unit tests verifying config overrides change the URL used for requests.
- Keep defaults identical to current behavior.
