from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from yarn_plugin.infrastructure.database import async_session_factory
from yarn_plugin.recommendations.domain.model.care_instructions import CareInstructions
from yarn_plugin.recommendations.domain.model.fiber_type import FiberType
from yarn_plugin.recommendations.domain.model.gauge import Gauge
from yarn_plugin.recommendations.domain.model.yarn import Yarn
from yarn_plugin.recommendations.domain.model.yarn_weight import YarnWeight
from yarn_plugin.recommendations.infrastructure.repository.orm.brand_orm import BrandModel
from yarn_plugin.recommendations.infrastructure.repository.orm.yarn_orm import YarnModel
from yarn_plugin.recommendations.infrastructure.repository.sqlalchemy_yarn_repository import SqlAlchemyYarnRepository


def make_yarn(brand_id: object, name: str, description: str, tags: list[str]) -> Yarn:
    return Yarn(
        brand_id=brand_id,  # type: ignore[arg-type]
        name=name,
        weight=YarnWeight.WORSTED,
        fiber_types=[FiberType.WOOL],
        gauge=Gauge(stitches=18, rows=24),
        care_instructions=CareInstructions(
            machine_washable=True,
            wash_temperature_celsius=30,
            wash_program="wool",
            bleach_allowed=False,
            tumble_dry_allowed=False,
            dry_clean_allowed=False,
            dry_flat=True,
            max_iron_temperature_celsius=110,
        ),
        description=description,
        tags=tags,
    )


@pytest.mark.asyncio
async def test_or_semantics_matches_on_partial_word_overlap() -> None:
    """Reproduces the exact query that returned zero results before the fix: not every word
    in "yarn for beginners" appears literally in the seeded content, but "beginners" should
    still be enough to find it once OR (not AND) semantics are used.
    """
    async with async_session_factory() as session:
        brand_id, yarn_id = await _seed_yarn(
            session, name="Full-Text Search Test Yarn", description="Great for beginners", tags=[]
        )
        try:
            repository = SqlAlchemyYarnRepository(session)
            results = await repository.search("yarn for beginners", limit=50)
            assert any(yarn.id == yarn_id for yarn in results)
        finally:
            await _cleanup(session, brand_id, yarn_id)


@pytest.mark.asyncio
async def test_single_letter_words_do_not_cause_spurious_matches() -> None:
    """Reproduces the false-positive found after switching to the 'simple' config: a bare "a"
    must not match content just because it contains the word "a" somewhere.
    """
    async with async_session_factory() as session:
        brand_id, yarn_id = await _seed_yarn(
            session,
            name="Full-Text Search Test Yarn 2",
            description="Comes with a silky feel",
            tags=[],
        )
        try:
            repository = SqlAlchemyYarnRepository(session)
            results = await repository.search("llana per a principiants", limit=50)
            assert not any(yarn.id == yarn_id for yarn in results)
        finally:
            await _cleanup(session, brand_id, yarn_id)


async def _seed_yarn(session: AsyncSession, name: str, description: str, tags: list[str]) -> tuple[object, object]:
    brand_id = uuid4()
    session.add(BrandModel(id=brand_id, name=f"Test Brand {uuid4()}", created_at=datetime.now(UTC)))
    await session.commit()

    repository = SqlAlchemyYarnRepository(session)
    yarn = make_yarn(brand_id, name, description, tags)
    await repository.save(yarn)
    return brand_id, yarn.id


async def _cleanup(session: AsyncSession, brand_id: object, yarn_id: object) -> None:
    await session.execute(delete(YarnModel).where(YarnModel.id == yarn_id))
    await session.execute(delete(BrandModel).where(BrandModel.id == brand_id))
    await session.commit()
