# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-XX

### Added
- Initial release of HERE Traffic SDK for Python
- Complete API coverage for Traffic API v7 (current)
  - Traffic flow endpoint (`GET /flow`)
  - Traffic incidents endpoint (`GET /incidents`)
  - Availability endpoint (`GET /availability`)
- Complete API coverage for Traffic API v6.3 (legacy)
  - Traffic flow endpoint (`GET /flow.json`)
  - Traffic incidents endpoint (`GET /incidents.json`)
- Complete API coverage for Traffic API v3 (legacy)
  - Traffic flow endpoint (`GET /flow`)
- Dual authentication support
  - API Key authentication
  - OAuth 2.0 authentication with automatic token management
- Response models with helper methods
  - `TrafficFlowResponse` with flow data accessors
  - `TrafficIncidentResponse` with filtering methods
  - `AvailabilityResponse` with availability information
- Geospatial filter utilities
  - Circle filters
  - Bounding box filters
  - Corridor/polyline filters
- Location referencing support
  - Shape points (coordinate-based)
  - TMC (Traffic Message Channel)
  - OLR (OpenLR Location Referencing)
- Comprehensive test suite
  - 100% code coverage
  - Unit tests (83 tests)
  - Integration tests (10 tests)
  - E2E tests (14 tests)
- Full type hints throughout
- Comprehensive documentation
  - API endpoint documentation
  - Authentication guide
  - Usage examples
  - Test coverage reports

### Features
- Convenience methods for common operations
- Error handling with proper exception types
- Automatic OAuth token refresh
- Support for additional query parameters
- Response model helper methods for data access

[1.0.0]: https://github.com/yourusername/here-traffic-sdk/releases/tag/v1.0.0

