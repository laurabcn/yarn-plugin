from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, field_validator
from sqlalchemy.ext.asyncio import AsyncSession

from yarn_plugin.infrastructure.database import get_session
from yarn_plugin.user_access.application.command.accept_invitation.command import AcceptInvitationCommand
from yarn_plugin.user_access.application.command.accept_invitation.handler import AcceptInvitationHandler
from yarn_plugin.user_access.domain.exception.invitation_already_used import InvitationAlreadyUsed
from yarn_plugin.user_access.domain.exception.invitation_expired import InvitationExpired
from yarn_plugin.user_access.domain.exception.invitation_not_found import InvitationNotFound
from yarn_plugin.user_access.infrastructure.repository.sqlalchemy_invitation_repository import (
    SqlAlchemyInvitationRepository,
)
from yarn_plugin.user_access.infrastructure.repository.sqlalchemy_user_repository import SqlAlchemyUserRepository
from yarn_plugin.user_access.infrastructure.security.password_service import PasswordService

router = APIRouter()


class AcceptInvitationRequest(BaseModel):
    token: str
    password: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class AcceptInvitationResponse(BaseModel):
    message: str
    email: str


@router.post("/auth/accept-invitation", response_model=AcceptInvitationResponse, status_code=status.HTTP_201_CREATED)
async def accept_invitation(
    body: AcceptInvitationRequest,
    session: AsyncSession = Depends(get_session),
) -> AcceptInvitationResponse:
    handler = AcceptInvitationHandler(
        invitation_repository=SqlAlchemyInvitationRepository(session),
        user_repository=SqlAlchemyUserRepository(session),
        password_service=PasswordService(),
    )
    try:
        user = await handler.handle(AcceptInvitationCommand(token=body.token, password=body.password))
    except InvitationNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invitation not found")
    except InvitationAlreadyUsed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invitation has already been used")
    except InvitationExpired:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invitation has expired")
    return AcceptInvitationResponse(message="Account created successfully. You can now log in.", email=user.email)