from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from yarn_plugin.infrastructure.database import get_session
from yarn_plugin.user_access.infrastructure.repository.sqlalchemy_invitation_repository import (
    SqlAlchemyInvitationRepository,
)

router = APIRouter()


class ValidateInvitationResponse(BaseModel):
    email: str
    expires_at: datetime


@router.get("/auth/invitation/{token}", response_model=ValidateInvitationResponse)
async def validate_invitation(
    token: str,
    session: AsyncSession = Depends(get_session),
) -> ValidateInvitationResponse:
    repository = SqlAlchemyInvitationRepository(session)
    invitation = await repository.find_by_token(token)
    if invitation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invitation not found")
    if invitation.is_used():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invitation has already been used")
    if invitation.is_expired():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invitation has expired")
    return ValidateInvitationResponse(email=invitation.email, expires_at=invitation.expires_at)