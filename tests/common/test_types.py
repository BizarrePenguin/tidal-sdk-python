from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from tidal_sdk.common.types import AccessToken


def test_access_token_is_immutable():
    token = AccessToken(
        token="abc",
        expires_at=datetime.now(UTC),
        scopes={"read"},
        user_id="user123",
    )

    with pytest.raises(FrozenInstanceError):
        token.token = "new"


def test_access_token_fields():
    expires = datetime.now(UTC)
    token = AccessToken(
        token="abc",
        expires_at=expires,
        scopes={"read", "write"},
    )

    assert token.token == "abc"
    assert token.expires_at == expires
    assert "read" in token.scopes
