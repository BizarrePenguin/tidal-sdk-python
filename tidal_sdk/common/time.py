"""
Time utilities for the TIDAL SDK.
"""

from datetime import UTC, datetime


def now_utc() -> datetime:
    """
    Returns the current UTC time.
    """
    return datetime.now(UTC)
