import secrets
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from yarn_plugin.config import settings
from yarn_plugin.user_access.application.command.create_invitation.command import CreateInvitationCommand
from yarn_plugin.user_access.domain.model.invitation import Invitation
from yarn_plugin.user_access.domain.repository.invitation_repository_interface import InvitationRepositoryInterface


@dataclass(frozen=True)
class CreateInvitationResult:
    invitation: Invitation
    invite_url: str


class CreateInvitationHandler:
    def __init__(self, invitation_repository: InvitationRepositoryInterface) -> None:
        self._invitation_repository = invitation_repository

    async def handle(self, command: CreateInvitationCommand) -> CreateInvitationResult:
        token = secrets.token_urlsafe(32)
        now = datetime.now(timezone.utc)
        invitation = Invitation(
            id=uuid.uuid4(),
            email=command.email,
            token=token,
            expires_at=now + timedelta(days=7),
            created_at=now,
        )
        await self._invitation_repository.save(invitation)
        invite_url = f"{settings.base_url}/accept?token={token}"
        return CreateInvitationResult(invitation=invitation, invite_url=invite_url)