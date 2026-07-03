from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from yarn_plugin.user_access.domain.model.user import User
from yarn_plugin.user_access.domain.repository.user_repository_interface import UserRepositoryInterface
from yarn_plugin.user_access.infrastructure.repository.orm.user_orm import UserModel


class SqlAlchemyUserRepository(UserRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, user: User) -> None:
        self._session.add(
            UserModel(
                id=user.id,
                email=user.email,
                password_hash=user.password_hash,
                invitation_id=user.invitation_id,
                created_at=user.created_at,
            )
        )
        await self._session.commit()

    async def find_by_email(self, email: str) -> User | None:
        result = await self._session.execute(select(UserModel).where(UserModel.email == email))
        row = result.scalar_one_or_none()
        return self._to_domain(row) if row else None

    def _to_domain(self, row: UserModel) -> User:
        return User(
            id=row.id,
            email=row.email,
            password_hash=row.password_hash,
            invitation_id=row.invitation_id,
            created_at=row.created_at,
        )