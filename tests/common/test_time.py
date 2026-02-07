from datetime import UTC

from tidal_sdk.common.time import now_utc


def test_now_utc_is_timezone_aware():
    now = now_utc()
    assert now.tzinfo is UTC
