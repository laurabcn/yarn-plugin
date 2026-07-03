from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from yarn_plugin.infrastructure.database import get_session
from yarn_plugin.shared.user_interface.http.admin_middleware import require_admin
from yarn_plugin.user_access.application.command.create_invitation.command import CreateInvitationCommand
from yarn_plugin.user_access.application.command.create_invitation.handler import CreateInvitationHandler
from yarn_plugin.user_access.infrastructure.repository.sqlalchemy_invitation_repository import (
    SqlAlchemyInvitationRepository,
)

router = APIRouter()


class CreateInvitationRequest(BaseModel):
    email: EmailStr


class InvitationStatusEnum(str):
    pending = "pending"
    accepted = "accepted"
    expired = "expired"


class InvitationResponse(BaseModel):
    id: UUID
    email: str
    token: str
    invite_url: str
    status: str
    expires_at: datetime
    accepted_at: datetime | None
    created_at: datetime


def _compute_status(expires_at: datetime, accepted_at: datetime | None) -> str:
    from datetime import timezone

    if accepted_at is not None:
        return "accepted"
    if datetime.now(timezone.utc) > expires_at.replace(tzinfo=timezone.utc):
        return "expired"
    return "pending"


@router.post("/admin/invitations", response_model=InvitationResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
async def create_invitation(
    body: CreateInvitationRequest,
    session: AsyncSession = Depends(get_session),
) -> InvitationResponse:
    repository = SqlAlchemyInvitationRepository(session)
    handler = CreateInvitationHandler(repository)
    result = await handler.handle(CreateInvitationCommand(email=body.email))
    inv = result.invitation
    return InvitationResponse(
        id=inv.id,
        email=inv.email,
        token=inv.token,
        invite_url=result.invite_url,
        status=_compute_status(inv.expires_at, inv.accepted_at),
        expires_at=inv.expires_at,
        accepted_at=inv.accepted_at,
        created_at=inv.created_at,
    )