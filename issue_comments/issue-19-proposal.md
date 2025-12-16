## Investigation
Response model properties like `TrafficFlowResponse.free_flow_speeds` append raw values from the API response without any coercion/validation. If the API returns strings/nulls (or a user passes mocked data), callers can get unexpected types.

## Proposed fix
- Add small, internal coercion helpers in `models.py` (e.g. `_coerce_float(value) -> Optional[float]`).
- Update response model properties to return well-typed values:
  - `free_flow_speeds`: `List[float]` filtered to values that can be coerced to float.
  - `expected_speeds`: same.
  - `available`: coerce common boolean representations.
- Keep the model tolerant: don’t raise on bad data, just omit/return defaults.

## Test plan
- Add/extend unit tests that feed string/None/bad values and assert the properties return only floats (or the expected default).
