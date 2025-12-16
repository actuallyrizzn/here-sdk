## Investigation
`AuthClient._get_oauth_token()` reads `_oauth_token` / `_token_expires_at` without synchronization, so concurrent threads can observe an expired/missing token at the same time and all call the token endpoint.

## Proposed fix
- Add a private lock on `AuthClient` (e.g. `threading.Lock`).
- Wrap the *entire* check-refresh-request-update sequence in the lock.
- Keep the current “refresh 5 minutes before expiry” behavior, but perform the validity check again once inside the lock (double-checked locking pattern).
- Ensure `refresh_token()` also participates in the same lock.

## Test plan
- Add a unit test that spawns multiple threads calling `get_auth_headers()` concurrently with an expired token and asserts `requests.post` is called exactly once.
- Keep existing unit tests for caching/expiry behavior green.
