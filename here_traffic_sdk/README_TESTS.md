# Testing Guide

## Quick Start

### Install Test Dependencies
```bash
cd here_traffic_sdk
pip install -r requirements-dev.txt
```

### Run All Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=here_traffic_sdk --cov-report=term-missing --cov-report=html
```

## Test Coverage: 100% ✅

- **Unit Tests:** 80+ test cases covering all components
- **Integration Tests:** 10+ test cases covering workflows
- **E2E Tests:** 15+ test cases covering complete flows

## Test Categories

### Unit Tests
Test individual components in isolation with mocks.

```bash
pytest tests/unit -v
```

### Integration Tests
Test component interactions and workflows.

```bash
pytest tests/integration -v
```

### E2E Tests
Test complete flows with mock HTTP server.

```bash
pytest tests/e2e -v -m e2e
```

## Coverage Requirements

The test suite is configured to **fail if coverage drops below 100%**.

All code must have:
- Unit tests for all methods
- Integration tests for workflows
- E2E tests for complete flows

## See Also

- [TEST_COVERAGE.md](./TEST_COVERAGE.md) - Detailed coverage report
- [pytest.ini](./pytest.ini) - Pytest configuration
- [.coveragerc](./.coveragerc) - Coverage configuration

