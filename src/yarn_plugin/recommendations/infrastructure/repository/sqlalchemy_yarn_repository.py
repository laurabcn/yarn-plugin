from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from yarn_plugin.recommendations.domain.model.ball_spec import BallSpec
from yarn_plugin.recommendations.domain.model.balls_requirement import BallsRequirement
from yarn_plugin.recommendations.domain.model.care_instructions import CareInstructions
from yarn_plugin.recommendations.domain.model.color import Color
from yarn_plugin.recommendations.domain.model.fiber_type import FiberType
from yarn_plugin.recommendations.domain.model.gauge import Gauge
from yarn_plugin.recommendations.domain.model.needle_size import NeedleSize
from yarn_plugin.recommendations.domain.model.sleeve_type import SleeveType
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
            fiber_types=[fiber_type.value for fiber_type in yarn.fiber_types],
            needle_min_mm=yarn.needle_size.min_mm if yarn.needle_size else None,
            needle_max_mm=yarn.needle_size.max_mm if yarn.needle_size else None,
            ball_weight_grams=yarn.ball_spec.weight_grams if yarn.ball_spec else None,
            ball_length_meters=yarn.ball_spec.length_meters if yarn.ball_spec else None,
            gauge_stitches=yarn.gauge.stitches,
            gauge_rows=yarn.gauge.rows,
            care_machine_washable=yarn.care_instructions.machine_washable,
            care_wash_temperature_celsius=yarn.care_instructions.wash_temperature_celsius,
            care_wash_program=yarn.care_instructions.wash_program,
            care_bleach_allowed=yarn.care_instructions.bleach_allowed,
            care_tumble_dry_allowed=yarn.care_instructions.tumble_dry_allowed,
            care_dry_clean_allowed=yarn.care_instructions.dry_clean_allowed,
            care_dry_flat=yarn.care_instructions.dry_flat,
            care_max_iron_temperature_celsius=yarn.care_instructions.max_iron_temperature_celsius,
            crochet_hook_size_mm=yarn.crochet_hook_size_mm,
            balls_per_garment=[
                {
                    "garment_size": requirement.garment_size,
                    "sleeve_type": requirement.sleeve_type.value,
                    "balls_needed": requirement.balls_needed,
                }
                for requirement in yarn.balls_per_garment
            ],
            colors=[{"code": color.code, "name": color.name} for color in yarn.colors],
            description=yarn.description,
            tags=yarn.tags,
            created_at=yarn.created_at,
        )
        self._session.add(orm)
        await self._session.commit()

    async def search(self, query: str, limit: int = 5) -> list[Yarn]:
        stmt = (
            select(YarnModel)
            .where(YarnModel.search_vector.op("@@")(func.plainto_tsquery("english", query)))
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
            fiber_types=[FiberType(value) for value in orm.fiber_types],
            needle_size=(
                NeedleSize(min_mm=orm.needle_min_mm, max_mm=orm.needle_max_mm)
                if orm.needle_min_mm is not None and orm.needle_max_mm is not None
                else None
            ),
            ball_spec=(
                BallSpec(weight_grams=orm.ball_weight_grams, length_meters=orm.ball_length_meters)
                if orm.ball_weight_grams is not None and orm.ball_length_meters is not None
                else None
            ),
            gauge=Gauge(stitches=orm.gauge_stitches, rows=orm.gauge_rows),
            care_instructions=CareInstructions(
                machine_washable=orm.care_machine_washable,
                wash_temperature_celsius=orm.care_wash_temperature_celsius,
                wash_program=orm.care_wash_program,
                bleach_allowed=orm.care_bleach_allowed,
                tumble_dry_allowed=orm.care_tumble_dry_allowed,
                dry_clean_allowed=orm.care_dry_clean_allowed,
                dry_flat=orm.care_dry_flat,
                max_iron_temperature_celsius=orm.care_max_iron_temperature_celsius,
            ),
            crochet_hook_size_mm=orm.crochet_hook_size_mm,
            balls_per_garment=[
                BallsRequirement(
                    garment_size=item["garment_size"],
                    sleeve_type=SleeveType(item["sleeve_type"]),
                    balls_needed=item["balls_needed"],
                )
                for item in orm.balls_per_garment
            ],
            colors=[Color(code=item["code"], name=item["name"]) for item in orm.colors],
            description=orm.description,
            tags=list(orm.tags or []),
            created_at=orm.created_at,
        )
