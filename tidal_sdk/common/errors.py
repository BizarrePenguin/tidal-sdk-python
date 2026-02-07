"""
Common error definitions for the TIDAL Python SDK.

All SDK-specific exceptions should inherit from TidalError.
"""


class TidalError(Exception):
    """
    Base class for all TIDAL SDK errors.
    """

    pass


class ConfigurationError(TidalError):
    """
    Raised when the SDK is misconfigured or used incorrectly.
    """

    pass


class NetworkError(TidalError):
    """
    Raised when a network-related failure occurs.
    """

    pass


class ApiError(TidalError):
    """
    Raised when the TIDAL backend responds with an error.
    """

    def __init__(self, status_code: int, message: str | None = None):
        self.status_code = status_code
        super().__init__(message or f"API error (status {status_code})")


class UnauthorizedError(ApiError):
    """
    Raised when authentication or authorization fails (HTTP 401/403).
    """

    pass


class RetryableError(TidalError):
    """
    Raised when an operation fails in a retryable way.
    """

    def __init__(self, error_code: str | None = None):
        self.error_code = error_code
        super().__init__(error_code)
