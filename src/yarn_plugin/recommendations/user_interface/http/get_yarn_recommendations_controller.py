from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from yarn_plugin.infrastructure.database import get_session
from yarn_plugin.recommendations.application.query.get_yarn_recommendations.handler import (
    GetYarnRecommendationsHandler,
)
from yarn_plugin.recommendations.application.query.get_yarn_recommendations.query import GetYarnRecommendationsQuery
from yarn_plugin.recommendations.infrastructure.repository.sqlalchemy_yarn_repository import SqlAlchemyYarnRepository

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


class YarnResponseModel(BaseModel):
    id: str
    name: str
    brand_id: str
    weight: str
    fiber_content: str
    description: str | None
    tags: list[str]


class YarnRecommendationsResponseModel(BaseModel):
    results: list[YarnResponseModel]
    total: int
    message: str


@router.get("/yarn", response_model=YarnRecommendationsResponseModel)
async def get_yarn_recommendations(
    query: str = Query(..., min_length=1, max_length=500, description="Natural language query"),
    limit: int = Query(default=5, ge=1, le=20),
    session: AsyncSession = Depends(get_session),
) -> YarnRecommendationsResponseModel:
    repository = SqlAlchemyYarnRepository(session)
    handler = GetYarnRecommendationsHandler(repository)
    response = await handler.handle(GetYarnRecommendationsQuery(query_text=query, limit=limit))

    return YarnRecommendationsResponseModel(
        results=[
            YarnResponseModel(
                id=str(dto.id),
                name=dto.name,
                brand_id=str(dto.brand_id),
                weight=dto.weight.value,
                fiber_content=dto.fiber_content,
                description=dto.description,
                tags=list(dto.tags),
            )
            for dto in response.results
        ],
        total=response.total,
        message=response.message,
    )
