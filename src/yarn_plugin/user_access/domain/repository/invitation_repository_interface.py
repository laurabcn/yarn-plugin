from abc import ABC, abstractmethod

from yarn_plugin.user_access.domain.model.invitation import Invitation


class InvitationRepositoryInterface(ABC):
    @abstractmethod
    async def save(self, invitation: Invitation) -> None: ...

    @abstractmethod
    async def find_by_token(self, token: str) -> Invitation | None: ...

    @abstractmethod
    async def find_all(self) -> list[Invitation]: ...
