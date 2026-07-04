from abc import ABC, abstractmethod
from uuid import UUID

from yarn_plugin.recommendations.domain.model.pattern import Pattern


class PatternRepositoryInterface(ABC):
    @abstractmethod
    async def save(self, pattern: Pattern) -> None: ...

    @abstractmethod
    async def search(self, query: str, limit: int = 5) -> list[Pattern]: ...

    @abstractmethod
    async def find_by_name_and_brand(self, name: str, brand_id: UUID) -> Pattern | None: ...
