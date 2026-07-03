from datetime import datetime, timedelta, timezone
from uuid import UUID

from jose import JWTError, jwt

from yarn_plugin.config import settings


class JwtService:
    _ALGORITHM = "HS256"

    def encode(self, user_id: UUID, email: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(hours=settings.jwt_expire_hours)
        payload = {"sub": str(user_id), "email": email, "exp": expire}
        return jwt.encode(payload, settings.jwt_secret, algorithm=self._ALGORITHM)

    def decode(self, token: str) -> dict[str, str]:
        try:
            return jwt.decode(token, settings.jwt_secret, algorithms=[self._ALGORITHM])
        except JWTError as e:
            raise ValueError("Invalid token") from e
