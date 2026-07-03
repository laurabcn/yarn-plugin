from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from yarn_plugin.user_access.domain.model.invitation import Invitation
from yarn_plugin.user_access.domain.repository.invitation_repository_interface import InvitationRepositoryInterface
from yarn_plugin.user_access.infrastructure.repository.orm.invitation_orm import InvitationModel


class SqlAlchemyInvitationRepository(InvitationRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, invitation: Invitation) -> None:
        existing = await self._session.get(InvitationModel, invitation.id)
        if existing:
            existing.accepted_at = invitation.accepted_at
        else:
            self._session.add(
                InvitationModel(
                    id=invitation.id,
                    email=invitation.email,
                    token=invitation.token,
                    expires_at=invitation.expires_at,
                    accepted_at=invitation.accepted_at,
                    created_at=invitation.created_at,
                )
            )
        await self._session.commit()

    async def find_by_token(self, token: str) -> Invitation | None:
        result = await self._session.execute(select(InvitationModel).where(InvitationModel.token == token))
        row = result.scalar_one_or_none()
        return self._to_domain(row) if row else None

    async def find_all(self) -> list[Invitation]:
        result = await self._session.execute(select(InvitationModel).order_by(InvitationModel.created_at.desc()))
        return [self._to_domain(row) for row in result.scalars().all()]

    def _to_domain(self, row: InvitationModel) -> Invitation:
        return Invitation(
            id=row.id,
            email=row.email,
            token=row.token,
            expires_at=row.expires_at,
            accepted_at=row.accepted_at,
            created_at=row.created_at,
        )