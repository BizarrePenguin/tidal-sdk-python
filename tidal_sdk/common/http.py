"""
HTTP client abstraction used by the TIDAL SDK.

Concrete implementations may be based on requests, httpx, aiohttp, etc.
"""

from collections.abc import Mapping
from typing import Any, Protocol


class HttpResponse:
    """
    Normalized HTTP response object.
    """

    def __init__(
        self,
        status_code: int,
        headers: Mapping[str, str],
        body: bytes,
    ):
        self.status_code = status_code
        self.headers = headers
        self.body = body


class HttpClient(Protocol):
    """
    Protocol defining the HTTP client interface used by the SDK.
    """

    def get(
        self,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, str] | None = None,
        timeout: float | None = None,
    ) -> HttpResponse: ...

    def post(
        self,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        data: Any | None = None,
        timeout: float | None = None,
    ) -> HttpResponse: ...
