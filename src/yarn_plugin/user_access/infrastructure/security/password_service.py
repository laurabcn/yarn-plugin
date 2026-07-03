from passlib.context import CryptContext

_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordService:
    def hash(self, password: str) -> str:
        return _ctx.hash(password)

    def verify(self, password: str, hashed: str) -> bool:
        return _ctx.verify(password, hashed)
