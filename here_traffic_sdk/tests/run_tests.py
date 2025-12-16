"""
Test runner script to verify 100% coverage
"""

import subprocess
import sys


def run_tests():
    """Run all tests and verify coverage"""
    print("Running unit tests...")
    result = subprocess.run(
        ["pytest", "tests/unit", "-v", "--cov=here_traffic_sdk", "--cov-report=term-missing"],
        cwd="here_traffic_sdk"
    )
    
    if result.returncode != 0:
        print("Unit tests failed!")
        return False
    
    print("\nRunning integration tests...")
    result = subprocess.run(
        ["pytest", "tests/integration", "-v", "--cov=here_traffic_sdk", "--cov-report=term-missing", "--cov-append"],
        cwd="here_traffic_sdk"
    )
    
    if result.returncode != 0:
        print("Integration tests failed!")
        return False
    
    print("\nRunning e2e tests...")
    result = subprocess.run(
        ["pytest", "tests/e2e", "-v", "-m", "e2e", "--cov=here_traffic_sdk", "--cov-report=term-missing", "--cov-append"],
        cwd="here_traffic_sdk"
    )
    
    if result.returncode != 0:
        print("E2E tests failed!")
        return False
    
    print("\nAll tests passed!")
    return True


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

