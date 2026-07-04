"""Seed the database with real, well-known yarn brands, yarns, and patterns.

Run inside the api container: docker compose exec api python scripts/seed.py
"""

import asyncio
from datetime import UTC, datetime
from uuid import uuid4

from yarn_plugin.infrastructure.database import async_session_factory
from yarn_plugin.recommendations.domain.model.care_instructions import CareInstructions
from yarn_plugin.recommendations.domain.model.difficulty import Difficulty
from yarn_plugin.recommendations.domain.model.fiber_type import FiberType
from yarn_plugin.recommendations.domain.model.gauge import Gauge
from yarn_plugin.recommendations.domain.model.language import Language
from yarn_plugin.recommendations.domain.model.needle_size import NeedleSize
from yarn_plugin.recommendations.domain.model.pattern import Pattern
from yarn_plugin.recommendations.domain.model.pattern_category import PatternCategory
from yarn_plugin.recommendations.domain.model.yarn import Yarn
from yarn_plugin.recommendations.domain.model.yarn_weight import YarnWeight
from yarn_plugin.recommendations.infrastructure.repository.orm.brand_orm import BrandModel
from yarn_plugin.recommendations.infrastructure.repository.sqlalchemy_pattern_repository import (
    SqlAlchemyPatternRepository,
)
from yarn_plugin.recommendations.infrastructure.repository.sqlalchemy_yarn_repository import (
    SqlAlchemyYarnRepository,
)

WOOL_CARE = CareInstructions(
    machine_washable=True,
    wash_temperature_celsius=30,
    wash_program="wool",
    bleach_allowed=False,
    tumble_dry_allowed=False,
    dry_clean_allowed=False,
    dry_flat=True,
    max_iron_temperature_celsius=110,
)

COTTON_CARE = CareInstructions(
    machine_washable=True,
    wash_temperature_celsius=40,
    wash_program="cotton",
    bleach_allowed=False,
    tumble_dry_allowed=True,
    dry_clean_allowed=False,
    dry_flat=False,
    max_iron_temperature_celsius=150,
)


async def seed() -> None:
    async with async_session_factory() as session:
        drops_id = uuid4()
        katia_id = uuid4()
        malabrigo_id = uuid4()

        session.add_all(
            [
                BrandModel(
                    id=drops_id,
                    name="Drops (Garnstudio)",
                    website="https://www.garnstudio.com",
                    description="Norwegian yarn brand known for affordable natural fibers and free patterns.",
                    created_at=datetime.now(UTC),
                ),
                BrandModel(
                    id=katia_id,
                    name="Katia",
                    website="https://www.katia.com",
                    description="Spanish yarn brand with a wide range of natural and blended fibers.",
                    created_at=datetime.now(UTC),
                ),
                BrandModel(
                    id=malabrigo_id,
                    name="Malabrigo",
                    website="https://malabrigoyarn.com",
                    description="Uruguayan hand-dyed yarn brand, known for luxurious merino wool.",
                    created_at=datetime.now(UTC),
                ),
            ]
        )
        await session.commit()

        yarn_repository = SqlAlchemyYarnRepository(session)
        pattern_repository = SqlAlchemyPatternRepository(session)

        drops_alaska = Yarn(
            id=uuid4(),
            brand_id=drops_id,
            name="Drops Alaska",
            weight=YarnWeight.ARAN,
            fiber_types=[FiberType.WOOL],
            gauge=Gauge(stitches=16, rows=22),
            needle_size=NeedleSize(min_mm=4.5, max_mm=5.5),
            ball_spec=None,
            care_instructions=WOOL_CARE,
            description="Rustic, warm Norwegian wool. Affordable and great for beginners.",
            tags=["beginner-friendly", "warm", "rustic", "natural"],
        )

        drops_nepal = Yarn(
            id=uuid4(),
            brand_id=drops_id,
            name="Drops Nepal",
            weight=YarnWeight.ARAN,
            fiber_types=[FiberType.WOOL, FiberType.ALPACA],
            gauge=Gauge(stitches=16, rows=22),
            needle_size=NeedleSize(min_mm=4.5, max_mm=5.5),
            care_instructions=WOOL_CARE,
            description="Wool-alpaca blend, extra soft with excellent stitch definition — popular for colorwork.",
            tags=["colorwork", "soft", "warm"],
        )

        drops_paris = Yarn(
            id=uuid4(),
            brand_id=drops_id,
            name="Drops Paris",
            weight=YarnWeight.ARAN,
            fiber_types=[FiberType.COTTON],
            gauge=Gauge(stitches=18, rows=24),
            needle_size=NeedleSize(min_mm=4.0, max_mm=5.0),
            care_instructions=COTTON_CARE,
            description="100% cotton, breathable — ideal for summer garments and dishcloths.",
            tags=["summer", "breathable", "washable"],
        )

        katia_concept = Yarn(
            id=uuid4(),
            brand_id=katia_id,
            name="Katia Concept Cotton-Cashmere",
            weight=YarnWeight.DK,
            fiber_types=[FiberType.COTTON, FiberType.CASHMERE],
            gauge=Gauge(stitches=22, rows=30),
            needle_size=NeedleSize(min_mm=3.5, max_mm=4.0),
            care_instructions=COTTON_CARE,
            description="Luxurious cotton-cashmere blend with a silky feel, drapes beautifully.",
            tags=["luxury", "soft", "lightweight"],
        )

        malabrigo_rios = Yarn(
            id=uuid4(),
            brand_id=malabrigo_id,
            name="Malabrigo Rios",
            weight=YarnWeight.WORSTED,
            fiber_types=[FiberType.MERINO_WOOL],
            gauge=Gauge(stitches=18, rows=24),
            needle_size=NeedleSize(min_mm=4.5, max_mm=5.5),
            care_instructions=WOOL_CARE,
            description="Hand-dyed 100% superwash merino, vibrant colorways, buttery soft.",
            tags=["hand-dyed", "luxury", "vibrant", "washable"],
        )

        for yarn in (drops_alaska, drops_nepal, drops_paris, katia_concept, malabrigo_rios):
            await yarn_repository.save(yarn)

        patterns = [
            Pattern(
                brand_id=drops_id,
                name="Beginner's Raglan Sweater",
                difficulty=Difficulty.BEGINNER,
                yarn_weight=YarnWeight.ARAN,
                category=PatternCategory.SWEATER,
                language=Language.ENGLISH,
                needle_size=NeedleSize(min_mm=4.5, max_mm=5.5),
                recommended_yarn_id=drops_alaska.id,
                popularity_rating=4.5,
                description="A simple top-down raglan sweater, perfect for a first garment project.",
                tags=["beginner-friendly", "cozy", "winter"],
            ),
            Pattern(
                brand_id=drops_id,
                name="Fair Isle Colorwork Hat",
                difficulty=Difficulty.INTERMEDIATE,
                yarn_weight=YarnWeight.ARAN,
                category=PatternCategory.HAT,
                language=Language.ENGLISH,
                needle_size=NeedleSize(min_mm=4.5, max_mm=5.5),
                recommended_yarn_id=drops_nepal.id,
                popularity_rating=4.8,
                description="A classic stranded colorwork hat pattern with a folded brim.",
                tags=["colorwork", "winter", "warm"],
            ),
            Pattern(
                brand_id=drops_id,
                name="Summer Lace Tank Top",
                difficulty=Difficulty.INTERMEDIATE,
                yarn_weight=YarnWeight.ARAN,
                category=PatternCategory.ACCESSORY,
                language=Language.ENGLISH,
                needle_size=NeedleSize(min_mm=4.0, max_mm=5.0),
                recommended_yarn_id=drops_paris.id,
                popularity_rating=4.2,
                description="A breathable lace-panel tank top in cotton, ideal for warm weather.",
                tags=["summer", "lace", "breathable"],
            ),
            Pattern(
                brand_id=katia_id,
                name="Cashmere Blend Baby Blanket",
                difficulty=Difficulty.BEGINNER,
                yarn_weight=YarnWeight.DK,
                category=PatternCategory.BLANKET,
                language=Language.SPANISH,
                needle_size=NeedleSize(min_mm=3.5, max_mm=4.0),
                recommended_yarn_id=katia_concept.id,
                popularity_rating=4.6,
                description="A soft garter-stitch baby blanket in a luxurious cotton-cashmere blend.",
                tags=["baby", "soft", "gift"],
            ),
            Pattern(
                brand_id=malabrigo_id,
                name="Chunky Cabled Cowl",
                difficulty=Difficulty.INTERMEDIATE,
                yarn_weight=YarnWeight.WORSTED,
                category=PatternCategory.ACCESSORY,
                language=Language.ENGLISH,
                needle_size=NeedleSize(min_mm=4.5, max_mm=5.5),
                recommended_yarn_id=malabrigo_rios.id,
                popularity_rating=4.9,
                description="A vibrant cabled cowl showcasing hand-dyed merino at its best.",
                tags=["cables", "colorful", "warm"],
            ),
        ]

        for pattern in patterns:
            await pattern_repository.save(pattern)

        print(f"Seeded 3 brands, 5 yarns, {len(patterns)} patterns.")


if __name__ == "__main__":
    asyncio.run(seed())
