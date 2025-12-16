## Investigation
The SDK currently accepts latitude/longitude/radius and raw geospatial filter strings with no range checking. It also forwards arbitrary `**kwargs` to `requests`, allowing unexpected param types/keys.

## Proposed fix
- Add validation helpers (latitude in [-90,90], longitude in [-180,180], radius positive and within a reasonable upper bound).
- Apply validation in:
  - `GeospatialFilter.circle/bbox/corridor`.
  - v6/v7 convenience methods that accept numeric inputs.
- Add a lightweight query-param sanitizer used by v3/v6/v7:
  - enforce param keys are strings
  - enforce values are JSON-serializable primitives (or lists of primitives)
  - reject nested dicts/objects

## Test plan
- Add unit tests for invalid lat/lon/radius raising `ValueError`.
- Add unit tests for kwargs sanitizer rejecting invalid key/value types.
