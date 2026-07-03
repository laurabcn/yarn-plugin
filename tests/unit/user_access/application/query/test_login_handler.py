import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest

from yarn_plugin.user_access.application.query.login.handler import LoginHandler
from yarn_plugin.user_access.application.query.login.query import LoginQuery
from yarn_plugin.user_access.domain.exception.invalid_credentials import InvalidCredentials
from yarn_plugin.user_access.domain.model.user import User
from yarn_plugin.user_access.infrastructure.security.jwt_service import JwtService
from yarn_plugin.user_access.infrastructure.security.password_service import PasswordService


def _make_user(password: str) -> User:
    ps = PasswordService()
    return User(
        id=uuid.uuid4(),
        email="katia@example.com",
        password_hash=ps.hash(password),
        invitation_id=uuid.uuid4(),
        created_at=datetime.now(timezone.utc),
    )


def _make_handler(user: User | None) -> LoginHandler:
    user_repo = AsyncMock()
    user_repo.find_by_email = AsyncMock(return_value=user)
    return LoginHandler(
        user_repository=user_repo,
        password_service=PasswordService(),
        jwt_service=JwtService(),
    )


async def test_returns_jwt_for_valid_credentials() -> None:
    user = _make_user("mysecretpass")
    handler = _make_handler(user)

    result = await handler.handle(LoginQuery(email="katia@example.com", password="mysecretpass"))

    assert result.access_token != ""
    assert result.token_type == "bearer"


async def test_raises_when_email_not_found() -> None:
    handler = _make_handler(None)

    with pytest.raises(InvalidCredentials):
        await handler.handle(LoginQuery(email="unknown@example.com", password="pass"))


async def test_raises_when_password_wrong() -> None:
    user = _make_user("correctpass")
    handler = _make_handler(user)

    with pytest.raises(InvalidCredentials):
        await handler.handle(LoginQuery(email="katia@example.com", password="wrongpass"))