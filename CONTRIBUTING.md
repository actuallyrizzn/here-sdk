# Contributing to HERE Traffic SDK

Thank you for your interest in contributing to the HERE Traffic SDK! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in the Issues section
2. If not, create a new issue with:
   - A clear, descriptive title
   - Steps to reproduce the bug
   - Expected vs. actual behavior
   - Environment details (Python version, OS, etc.)
   - Any relevant error messages or logs

### Suggesting Features

1. Check if the feature has already been suggested
2. Create a new issue with:
   - A clear description of the feature
   - Use cases and examples
   - Potential implementation approach (if you have ideas)

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the code style and conventions
   - Add tests for new functionality
   - Update documentation as needed
   - Ensure all tests pass

4. **Maintain 100% test coverage**
   - All new code must have tests
   - Run `pytest --cov=here_traffic_sdk --cov-fail-under=100` to verify

5. **Commit your changes**
   ```bash
   git commit -m "Add: Description of your changes"
   ```
   Use clear, descriptive commit messages.

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear description of your changes
   - Reference any related issues
   - Ensure CI checks pass

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip
- git

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/yourusername/here-traffic-sdk.git
cd here-traffic-sdk

# Navigate to SDK directory
cd here_traffic_sdk

# Install in development mode
pip install -e .

# Install test dependencies
pip install -r requirements-dev.txt
```

### Pre-commit Hooks

This repo uses [pre-commit](https://pre-commit.com/) to run formatting and lint checks automatically.

```bash
# Install git hooks
pre-commit install

# (Optional) Run on all files
pre-commit run --all-files
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=here_traffic_sdk --cov-report=html

# Run specific test categories
pytest tests/unit -v
pytest tests/integration -v
pytest tests/e2e -v -m e2e
```

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for all functions
- Write docstrings for all public functions and classes
- Keep functions focused and single-purpose

### Test Requirements

- **100% test coverage is required**
- All new code must have:
  - Unit tests
  - Integration tests (if applicable)
  - E2E tests (if applicable)
- Tests must pass before submitting PR

## Documentation

- Update README.md if adding new features
- Add examples to the examples/ directory
- Update API documentation in docs/ if endpoints change
- Keep docstrings up to date

## License

By contributing, you agree that your contributions will be licensed under the same license as the project:
- Code: AGPL-3.0
- Documentation: CC BY-SA 4.0

## Questions?

Feel free to open an issue for questions or reach out to the maintainers.

Thank you for contributing! 🎉

