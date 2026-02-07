"""
Shared types used across multiple SDK modules.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AccessToken:
    """
    Represents an OAuth access token.
    """

    token: str
    expires_at: datetime
    scopes: set[str]
    user_id: str | None = None
