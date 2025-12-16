"""
Unit tests for SDK version export.
"""

from here_traffic_sdk import __version__
from here_traffic_sdk._version import __version__ as internal_version


def test_version_exported():
    assert __version__ == internal_version
    assert isinstance(__version__, str)
    assert __version__

