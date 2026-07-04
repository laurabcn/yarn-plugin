from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from yarn_plugin.infrastructure.database import get_session
from yarn_plugin.recommendations.application.query.get_yarn_recommendations.handler import (
    GetYarnRecommendationsHandler,
)
from yarn_plugin.recommendations.application.query.get_yarn_recommendations.query import GetYarnRecommendationsQuery
from yarn_plugin.recommendations.application.query.get_yarn_recommendations.response import YarnDto
from yarn_plugin.recommendations.infrastructure.repository.sqlalchemy_yarn_repository import SqlAlchemyYarnRepository

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


class GaugeResponseModel(BaseModel):
    stitches: int
    rows: int


class NeedleSizeResponseModel(BaseModel):
    min_mm: float
    max_mm: float


class BallSpecResponseModel(BaseModel):
    weight_grams: int
    length_meters: int


class CareInstructionsResponseModel(BaseModel):
    machine_washable: bool
    wash_temperature_celsius: int | None
    wash_program: str | None
    bleach_allowed: bool
    tumble_dry_allowed: bool
    dry_clean_allowed: bool
    dry_flat: bool
    max_iron_temperature_celsius: int | None


class ColorResponseModel(BaseModel):
    code: str
    name: str | None


class BallsRequirementResponseModel(BaseModel):
    garment_size: str
    sleeve_type: str
    balls_needed: int


class YarnResponseModel(BaseModel):
    id: str
    name: str
    brand_id: str
    weight: str
    fiber_types: list[str]
    gauge: GaugeResponseModel
    care_instructions: CareInstructionsResponseModel
    description: str | None
    needle_size: NeedleSizeResponseModel | None
    ball_spec: BallSpecResponseModel | None
    crochet_hook_size_mm: float | None
    tags: list[str]
    colors: list[ColorResponseModel]
    balls_per_garment: list[BallsRequirementResponseModel]


class YarnRecommendationsResponseModel(BaseModel):
    results: list[YarnResponseModel]
    total: int
    message: str


def yarn_dto_to_response_model(dto: YarnDto) -> YarnResponseModel:
    return YarnResponseModel(
        id=str(dto.id),
        name=dto.name,
        brand_id=str(dto.brand_id),
        weight=dto.weight.value,
        fiber_types=[fiber_type.value for fiber_type in dto.fiber_types],
        gauge=GaugeResponseModel(stitches=dto.gauge.stitches, rows=dto.gauge.rows),
        care_instructions=CareInstructionsResponseModel(
            machine_washable=dto.care_instructions.machine_washable,
            wash_temperature_celsius=dto.care_instructions.wash_temperature_celsius,
            wash_program=dto.care_instructions.wash_program,
            bleach_allowed=dto.care_instructions.bleach_allowed,
            tumble_dry_allowed=dto.care_instructions.tumble_dry_allowed,
            dry_clean_allowed=dto.care_instructions.dry_clean_allowed,
            dry_flat=dto.care_instructions.dry_flat,
            max_iron_temperature_celsius=dto.care_instructions.max_iron_temperature_celsius,
        ),
        description=dto.description,
        needle_size=(
            NeedleSizeResponseModel(min_mm=dto.needle_size.min_mm, max_mm=dto.needle_size.max_mm)
            if dto.needle_size
            else None
        ),
        ball_spec=(
            BallSpecResponseModel(weight_grams=dto.ball_spec.weight_grams, length_meters=dto.ball_spec.length_meters)
            if dto.ball_spec
            else None
        ),
        crochet_hook_size_mm=dto.crochet_hook_size_mm,
        tags=list(dto.tags),
        colors=[ColorResponseModel(code=color.code, name=color.name) for color in dto.colors],
        balls_per_garment=[
            BallsRequirementResponseModel(
                garment_size=requirement.garment_size,
                sleeve_type=requirement.sleeve_type.value,
                balls_needed=requirement.balls_needed,
            )
            for requirement in dto.balls_per_garment
        ],
    )


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
        results=[yarn_dto_to_response_model(dto) for dto in response.results],
        total=response.total,
        message=response.message,
    )
