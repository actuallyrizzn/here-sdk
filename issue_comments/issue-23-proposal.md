## Proposed fix
- Add `.pre-commit-config.yaml` with:
  - `ruff` (lint + autofix)
  - `black` (format)
  - basic hygiene hooks (trailing whitespace, end-of-file-fixer, check-yaml)
- Document setup in `CONTRIBUTING.md` (install + `pre-commit install`).

## Test plan
- Run `pre-commit run --all-files` locally in CI/dev.
