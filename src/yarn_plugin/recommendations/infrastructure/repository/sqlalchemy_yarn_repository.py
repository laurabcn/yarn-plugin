from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from yarn_plugin.recommendations.domain.model.yarn import Yarn
from yarn_plugin.recommendations.domain.model.yarn_weight import YarnWeight
from yarn_plugin.recommendations.domain.repository.yarn_repository_interface import YarnRepositoryInterface
from yarn_plugin.recommendations.infrastructure.repository.orm.yarn_orm import YarnModel


class SqlAlchemyYarnRepository(YarnRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, yarn: Yarn) -> None:
        orm = YarnModel(
            id=yarn.id,
            brand_id=yarn.brand_id,
            name=yarn.name,
            weight=yarn.weight.value,
            fiber_content=yarn.fiber_content,
            description=yarn.description,
            tags=yarn.tags,
            created_at=yarn.created_at,
        )
        self._session.add(orm)
        await self._session.commit()

    async def search(self, query: str, limit: int = 5) -> list[Yarn]:
        stmt = (
            select(YarnModel)
            .where(
                func.to_tsvector("english", YarnModel.search_vector).op("@@")(
                    func.plainto_tsquery("english", query)
                )
            )
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(row) for row in result.scalars().all()]

    async def find_by_name_and_brand(self, name: str, brand_id: UUID) -> Yarn | None:
        stmt = select(YarnModel).where(YarnModel.name == name, YarnModel.brand_id == brand_id)
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        return self._to_domain(row) if row else None

    def _to_domain(self, orm: YarnModel) -> Yarn:
        return Yarn(
            id=orm.id,
            brand_id=orm.brand_id,
            name=orm.name,
            weight=YarnWeight(orm.weight),
            fiber_content=orm.fiber_content,
            description=orm.description,
            tags=list(orm.tags or []),
            created_at=orm.created_at,
        )
