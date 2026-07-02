from abc import ABC, abstractmethod
from uuid import UUID

from yarn_plugin.recommendations.domain.model.yarn import Yarn


class YarnRepositoryInterface(ABC):
    @abstractmethod
    async def save(self, yarn: Yarn) -> None: ...

    @abstractmethod
    async def search(self, query: str, limit: int = 5) -> list[Yarn]: ...

    @abstractmethod
    async def find_by_name_and_brand(self, name: str, brand_id: UUID) -> Yarn | None: ...