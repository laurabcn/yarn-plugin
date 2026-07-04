from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from yarn_plugin.recommendations.domain.model.difficulty import Difficulty
from yarn_plugin.recommendations.domain.model.language import Language
from yarn_plugin.recommendations.domain.model.needle_size import NeedleSize
from yarn_plugin.recommendations.domain.model.pattern import Pattern
from yarn_plugin.recommendations.domain.model.pattern_category import PatternCategory
from yarn_plugin.recommendations.domain.model.yarn_weight import YarnWeight
from yarn_plugin.recommendations.domain.repository.pattern_repository_interface import (
    PatternRepositoryInterface,
)
from yarn_plugin.recommendations.infrastructure.repository.orm.pattern_orm import PatternModel


class SqlAlchemyPatternRepository(PatternRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, pattern: Pattern) -> None:
        orm = PatternModel(
            id=pattern.id,
            brand_id=pattern.brand_id,
            name=pattern.name,
            difficulty=pattern.difficulty.value,
            yarn_weight=pattern.yarn_weight.value,
            category=pattern.category.value,
            language=pattern.language.value,
            needle_min_mm=pattern.needle_size.min_mm,
            needle_max_mm=pattern.needle_size.max_mm,
            recommended_yarn_id=pattern.recommended_yarn_id,
            popularity_rating=pattern.popularity_rating,
            description=pattern.description,
            tags=pattern.tags,
            created_at=pattern.created_at,
        )
        self._session.add(orm)
        await self._session.commit()

    async def search(self, query: str, limit: int = 5) -> list[Pattern]:
        stmt = (
            select(PatternModel)
            .where(PatternModel.search_vector.op("@@")(func.plainto_tsquery("english", query)))
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(row) for row in result.scalars().all()]

    async def find_by_name_and_brand(self, name: str, brand_id: UUID) -> Pattern | None:
        stmt = select(PatternModel).where(PatternModel.name == name, PatternModel.brand_id == brand_id)
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        return self._to_domain(row) if row else None

    def _to_domain(self, orm: PatternModel) -> Pattern:
        return Pattern(
            id=orm.id,
            brand_id=orm.brand_id,
            name=orm.name,
            difficulty=Difficulty(orm.difficulty),
            yarn_weight=YarnWeight(orm.yarn_weight),
            category=PatternCategory(orm.category),
            language=Language(orm.language),
            needle_size=NeedleSize(min_mm=orm.needle_min_mm, max_mm=orm.needle_max_mm),
            recommended_yarn_id=orm.recommended_yarn_id,
            popularity_rating=orm.popularity_rating,
            description=orm.description,
            tags=list(orm.tags or []),
            created_at=orm.created_at,
        )
