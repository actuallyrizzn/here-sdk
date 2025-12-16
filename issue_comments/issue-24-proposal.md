## Proposed fix
- Add a repository-root `pyproject.toml` configuring:
  - `black` (line length, target versions)
  - `ruff` (ruleset + exclusions)
  - `mypy` (strict-ish defaults appropriate for this repo)
  - `pytest` (optional centralization; keep existing `pytest.ini` if preferred)

## Test plan
- Ensure `ruff`, `black --check`, and `mypy` can run cleanly on the repo.
