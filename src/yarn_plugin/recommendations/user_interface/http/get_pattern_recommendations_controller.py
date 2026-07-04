from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from yarn_plugin.infrastructure.database import get_session
from yarn_plugin.recommendations.application.query.get_pattern_recommendations.handler import (
    GetPatternRecommendationsHandler,
)
from yarn_plugin.recommendations.application.query.get_pattern_recommendations.query import (
    GetPatternRecommendationsQuery,
)
from yarn_plugin.recommendations.application.query.get_pattern_recommendations.response import PatternDto
from yarn_plugin.recommendations.infrastructure.repository.sqlalchemy_pattern_repository import (
    SqlAlchemyPatternRepository,
)

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


class NeedleSizeResponseModel(BaseModel):
    min_mm: float
    max_mm: float


class PatternResponseModel(BaseModel):
    id: str
    name: str
    brand_id: str
    difficulty: str
    yarn_weight: str
    category: str
    language: str
    needle_size: NeedleSizeResponseModel
    recommended_yarn_id: str | None
    popularity_rating: float | None
    description: str | None
    tags: list[str]


class PatternRecommendationsResponseModel(BaseModel):
    results: list[PatternResponseModel]
    total: int
    message: str


def pattern_dto_to_response_model(dto: PatternDto) -> PatternResponseModel:
    return PatternResponseModel(
        id=str(dto.id),
        name=dto.name,
        brand_id=str(dto.brand_id),
        difficulty=dto.difficulty.value,
        yarn_weight=dto.yarn_weight.value,
        category=dto.category.value,
        language=dto.language.value,
        needle_size=NeedleSizeResponseModel(min_mm=dto.needle_size.min_mm, max_mm=dto.needle_size.max_mm),
        recommended_yarn_id=str(dto.recommended_yarn_id) if dto.recommended_yarn_id else None,
        popularity_rating=dto.popularity_rating,
        description=dto.description,
        tags=list(dto.tags),
    )


@router.get("/patterns", response_model=PatternRecommendationsResponseModel)
async def get_pattern_recommendations(
    query: str = Query(..., min_length=1, max_length=500, description="Natural language query"),
    limit: int = Query(default=5, ge=1, le=20),
    session: AsyncSession = Depends(get_session),
) -> PatternRecommendationsResponseModel:
    repository = SqlAlchemyPatternRepository(session)
    handler = GetPatternRecommendationsHandler(repository)
    response = await handler.handle(GetPatternRecommendationsQuery(query_text=query, limit=limit))

    return PatternRecommendationsResponseModel(
        results=[pattern_dto_to_response_model(dto) for dto in response.results],
        total=response.total,
        message=response.message,
    )
