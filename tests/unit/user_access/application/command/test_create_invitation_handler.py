import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from yarn_plugin.user_access.application.command.create_invitation.command import CreateInvitationCommand
from yarn_plugin.user_access.application.command.create_invitation.handler import CreateInvitationHandler
from yarn_plugin.user_access.domain.model.invitation import Invitation


@pytest.fixture()
def invitation_repository() -> AsyncMock:
    repo = AsyncMock()
    repo.save = AsyncMock()
    return repo


@pytest.fixture()
def handler(invitation_repository: AsyncMock) -> CreateInvitationHandler:
    return CreateInvitationHandler(invitation_repository=invitation_repository)


async def test_creates_invitation_with_token(handler: CreateInvitationHandler, invitation_repository: AsyncMock) -> None:
    result = await handler.handle(CreateInvitationCommand(email="katia@example.com"))

    assert result.invitation.email == "katia@example.com"
    assert len(result.invitation.token) > 0
    assert result.invitation.accepted_at is None
    invitation_repository.save.assert_called_once()


async def test_invite_url_contains_token(handler: CreateInvitationHandler) -> None:
    result = await handler.handle(CreateInvitationCommand(email="katia@example.com"))

    assert result.invitation.token in result.invite_url


async def test_invitation_expires_in_seven_days(handler: CreateInvitationHandler) -> None:
    result = await handler.handle(CreateInvitationCommand(email="katia@example.com"))

    delta = result.invitation.expires_at - result.invitation.created_at
    assert timedelta(days=6) < delta <= timedelta(days=7)