from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from yarn_plugin.infrastructure.database import get_session
from yarn_plugin.user_access.application.query.login.handler import LoginHandler
from yarn_plugin.user_access.application.query.login.query import LoginQuery
from yarn_plugin.user_access.domain.exception.invalid_credentials import InvalidCredentials
from yarn_plugin.user_access.infrastructure.repository.sqlalchemy_user_repository import SqlAlchemyUserRepository
from yarn_plugin.user_access.infrastructure.security.jwt_service import JwtService
from yarn_plugin.user_access.infrastructure.security.password_service import PasswordService

router = APIRouter()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


@router.post("/auth/login", response_model=LoginResponse)
async def login(
    body: LoginRequest,
    session: AsyncSession = Depends(get_session),
) -> LoginResponse:
    handler = LoginHandler(
        user_repository=SqlAlchemyUserRepository(session),
        password_service=PasswordService(),
        jwt_service=JwtService(),
    )
    try:
        result = await handler.handle(LoginQuery(email=body.email, password=body.password))
    except InvalidCredentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return LoginResponse(access_token=result.access_token, token_type=result.token_type)