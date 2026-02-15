"""Minimal auth package for the TIDAL SDK.

This package implements a small subset of the Auth specification focused on
acquiring an application token using the OAuth2 client credentials flow.
"""

from .auth import Auth  # re-export for convenience

__all__ = ["Auth"]
