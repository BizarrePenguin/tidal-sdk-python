import os
from datetime import UTC, datetime

import pytest

from tidal_sdk.auth import Auth


def _env_or_skip():
    client_id = os.getenv("TIDAL_CLIENT_ID")
    client_secret = os.getenv("TIDAL_CLIENT_SECRET")
    if not client_id or not client_secret:
        pytest.skip("TIDAL_CLIENT_ID/TIDAL_CLIENT_SECRET not set in environment")
    return client_id, client_secret


@pytest.mark.integration
def test_client_credentials_flow_integration():
    client_id, client_secret = _env_or_skip()
    token_url = os.getenv("TIDAL_TOKEN_URL")  # optional override

    auth = Auth(client_id=client_id, client_secret=client_secret, token_url=token_url)
    token = auth.get_client_token()

    assert token.token and isinstance(token.token, str)
    assert isinstance(token.expires_at, datetime)
    assert token.expires_at > datetime.now(UTC)