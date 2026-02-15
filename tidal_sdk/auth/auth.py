"""Auth module implementing client-credentials flow (minimal).

This is a small, implementation-focused subset intended to allow integration
tests to exercise real TIDAL authentication using client id/secret.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timedelta

import httpx

from tidal_sdk.common.errors import ConfigurationError, NetworkError
from tidal_sdk.common.time import now_utc
from tidal_sdk.common.types import AccessToken


@dataclass
class _TokenData:
    token: str
    expires_at: datetime
    scopes: set[str]


class Auth:
    """Minimal Auth implementation: client credentials only.

    Args:
        client_id: OAuth client id. If not provided, read from
            `TIDAL_CLIENT_ID` env var.
        client_secret: OAuth client secret. If not provided, read from
            `TIDAL_CLIENT_SECRET` env var.
        token_url: Optional token endpoint URL override. Defaults to
            `https://auth.tidal.com/v1/oauth2/token`.
    """

    DEFAULT_TOKEN_URL = "https://auth.tidal.com/v1/oauth2/token"

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        token_url: str | None = None,
        timeout: float = 10.0,
    ) -> None:
        self.client_id = client_id or os.getenv("TIDAL_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("TIDAL_CLIENT_SECRET")
        if not self.client_id or not self.client_secret:
            raise ConfigurationError(
                "client_id and client_secret must be provided either as arguments or via environment"
            )

        self.token_url = token_url or os.getenv("TIDAL_TOKEN_URL") or self.DEFAULT_TOKEN_URL
        self._timeout = timeout
        self._cached: _TokenData | None = None

    def _is_token_valid(self) -> bool:
        if not self._cached:
            return False
        return now_utc() + timedelta(seconds=10) < self._cached.expires_at

    def get_client_token(self) -> AccessToken:
        """Return an application access token (client credentials).

        Caches the token until close to expiration.
        """
        if self._cached and self._is_token_valid():
            return AccessToken(
                token=self._cached.token,
                expires_at=self._cached.expires_at,
                scopes=self._cached.scopes,
            )

        try:
            with httpx.Client(timeout=self._timeout) as client:
                headers = {"Accept": "application/json"}
                data = {
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                }

                resp = client.post(self.token_url, data=data, headers=headers)
        except httpx.RequestError as exc:  # network problems
            raise NetworkError(str(exc)) from exc

        if resp.status_code != 200:
            raise NetworkError(f"token endpoint returned status {resp.status_code}")

        body = resp.json()
        access_token = body.get("access_token")
        expires_in = body.get("expires_in", 3600)
        scope_str = body.get("scope", "")

        if not access_token:
            raise NetworkError("token response missing access_token")

        expires_at = now_utc() + timedelta(seconds=int(expires_in))
        scopes = set(scope_str.split()) if scope_str else set()

        self._cached = _TokenData(token=access_token, expires_at=expires_at, scopes=scopes)

        return AccessToken(token=access_token, expires_at=expires_at, scopes=scopes)
