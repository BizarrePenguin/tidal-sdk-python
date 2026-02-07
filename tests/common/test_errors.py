from tidal_sdk.common.errors import (
    ApiError,
    ConfigurationError,
    NetworkError,
    RetryableError,
    TidalError,
    UnauthorizedError,
)


def test_error_hierarchy():
    assert issubclass(ConfigurationError, TidalError)
    assert issubclass(NetworkError, TidalError)
    assert issubclass(ApiError, TidalError)
    assert issubclass(UnauthorizedError, ApiError)
    assert issubclass(RetryableError, TidalError)


def test_api_error_contains_status_code():
    err = ApiError(401, "Unauthorized")
    assert err.status_code == 401
    assert "Unauthorized" in str(err)


def test_retryable_error_optional_code():
    err = RetryableError("temporary_failure")
    assert err.error_code == "temporary_failure"
