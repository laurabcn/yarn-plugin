from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from yarn_plugin.config import settings
from yarn_plugin.infrastructure.database import get_session
from yarn_plugin.shared.user_interface.http.admin_middleware import require_admin
from yarn_plugin.user_access.infrastructure.repository.sqlalchemy_invitation_repository import (
    SqlAlchemyInvitationRepository,
)

router = APIRouter()


class InvitationListItem(BaseModel):
    id: UUID
    email: str
    token: str
    invite_url: str
    status: str
    expires_at: datetime
    accepted_at: datetime | None
    created_at: datetime


def _compute_status(expires_at: datetime, accepted_at: datetime | None) -> str:
    if accepted_at is not None:
        return "accepted"
    if datetime.now(timezone.utc) > expires_at.replace(tzinfo=timezone.utc):
        return "expired"
    return "pending"


@router.get("/admin/invitations", response_model=list[InvitationListItem], status_code=status.HTTP_200_OK, dependencies=[Depends(require_admin)])
async def list_invitations(session: AsyncSession = Depends(get_session)) -> list[InvitationListItem]:
    repository = SqlAlchemyInvitationRepository(session)
    invitations = await repository.find_all()
    return [
        InvitationListItem(
            id=inv.id,
            email=inv.email,
            token=inv.token,
            invite_url=f"{settings.base_url}/accept?token={inv.token}",
            status=_compute_status(inv.expires_at, inv.accepted_at),
            expires_at=inv.expires_at,
            accepted_at=inv.accepted_at,
            created_at=inv.created_at,
        )
        for inv in invitations
    ]