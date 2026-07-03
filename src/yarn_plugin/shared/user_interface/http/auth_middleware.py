from dataclasses import dataclass
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from yarn_plugin.user_access.infrastructure.security.jwt_service import JwtService

_bearer = HTTPBearer()


@dataclass(frozen=True)
class CurrentUser:
    user_id: UUID
    email: str


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    jwt_service: JwtService = Depends(JwtService),
) -> CurrentUser:
    try:
        payload = jwt_service.decode(credentials.credentials)
        return CurrentUser(user_id=UUID(payload["sub"]), email=payload["email"])
    except (ValueError, KeyError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")