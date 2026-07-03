import uuid
from datetime import datetime, timezone

from yarn_plugin.user_access.application.command.accept_invitation.command import AcceptInvitationCommand
from yarn_plugin.user_access.domain.exception.invitation_already_used import InvitationAlreadyUsed
from yarn_plugin.user_access.domain.exception.invitation_expired import InvitationExpired
from yarn_plugin.user_access.domain.exception.invitation_not_found import InvitationNotFound
from yarn_plugin.user_access.domain.model.user import User
from yarn_plugin.user_access.domain.repository.invitation_repository_interface import InvitationRepositoryInterface
from yarn_plugin.user_access.domain.repository.user_repository_interface import UserRepositoryInterface
from yarn_plugin.user_access.infrastructure.security.password_service import PasswordService


class AcceptInvitationHandler:
    def __init__(
        self,
        invitation_repository: InvitationRepositoryInterface,
        user_repository: UserRepositoryInterface,
        password_service: PasswordService,
    ) -> None:
        self._invitation_repository = invitation_repository
        self._user_repository = user_repository
        self._password_service = password_service

    async def handle(self, command: AcceptInvitationCommand) -> User:
        invitation = await self._invitation_repository.find_by_token(command.token)
        if invitation is None:
            raise InvitationNotFound()
        if invitation.is_used():
            raise InvitationAlreadyUsed()
        if invitation.is_expired():
            raise InvitationExpired()

        password_hash = self._password_service.hash(command.password)
        user = User(
            id=uuid.uuid4(),
            email=invitation.email,
            password_hash=password_hash,
            invitation_id=invitation.id,
            created_at=datetime.now(timezone.utc),
        )
        await self._user_repository.save(user)

        invitation.accept()
        await self._invitation_repository.save(invitation)

        return user