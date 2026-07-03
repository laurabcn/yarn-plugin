import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock

import pytest

from yarn_plugin.user_access.application.command.accept_invitation.command import AcceptInvitationCommand
from yarn_plugin.user_access.application.command.accept_invitation.handler import AcceptInvitationHandler
from yarn_plugin.user_access.domain.exception.invitation_already_used import InvitationAlreadyUsed
from yarn_plugin.user_access.domain.exception.invitation_expired import InvitationExpired
from yarn_plugin.user_access.domain.exception.invitation_not_found import InvitationNotFound
from yarn_plugin.user_access.domain.model.invitation import Invitation
from yarn_plugin.user_access.infrastructure.security.password_service import PasswordService


def _make_invitation(*, accepted_at: datetime | None = None, days_offset: int = 7) -> Invitation:
    now = datetime.now(timezone.utc)
    return Invitation(
        id=uuid.uuid4(),
        email="katia@example.com",
        token="valid-token",
        expires_at=now + timedelta(days=days_offset),
        created_at=now,
        accepted_at=accepted_at,
    )


def _make_handler(invitation: Invitation | None) -> tuple[AcceptInvitationHandler, AsyncMock, AsyncMock]:
    inv_repo = AsyncMock()
    inv_repo.find_by_token = AsyncMock(return_value=invitation)
    inv_repo.save = AsyncMock()
    user_repo = AsyncMock()
    user_repo.save = AsyncMock()
    handler = AcceptInvitationHandler(
        invitation_repository=inv_repo,
        user_repository=user_repo,
        password_service=PasswordService(),
    )
    return handler, inv_repo, user_repo


async def test_creates_user_for_valid_invitation() -> None:
    invitation = _make_invitation()
    handler, inv_repo, user_repo = _make_handler(invitation)

    user = await handler.handle(AcceptInvitationCommand(token="valid-token", password="securepass"))

    assert user.email == "katia@example.com"
    user_repo.save.assert_called_once()
    inv_repo.save.assert_called()


async def test_raises_when_invitation_not_found() -> None:
    handler, _, _ = _make_handler(None)

    with pytest.raises(InvitationNotFound):
        await handler.handle(AcceptInvitationCommand(token="bad-token", password="securepass"))


async def test_raises_when_invitation_already_used() -> None:
    used_invitation = _make_invitation(accepted_at=datetime.now(timezone.utc))
    handler, _, _ = _make_handler(used_invitation)

    with pytest.raises(InvitationAlreadyUsed):
        await handler.handle(AcceptInvitationCommand(token="valid-token", password="securepass"))


async def test_raises_when_invitation_expired() -> None:
    expired_invitation = _make_invitation(days_offset=-1)
    handler, _, _ = _make_handler(expired_invitation)

    with pytest.raises(InvitationExpired):
        await handler.handle(AcceptInvitationCommand(token="valid-token", password="securepass"))