"""
Official TIDAL Python SDK.

This package provides access to TIDAL APIs, authentication flows,
and playback-related functionality.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("tidal-sdk")
except PackageNotFoundError:
    # Package is not installed (e.g. running from source)
    __version__ = "0.0.0"

__all__ = ["__version__"]
