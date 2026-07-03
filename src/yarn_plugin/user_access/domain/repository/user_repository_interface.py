from abc import ABC, abstractmethod

from yarn_plugin.user_access.domain.model.user import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def save(self, user: User) -> None: ...

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None: ...