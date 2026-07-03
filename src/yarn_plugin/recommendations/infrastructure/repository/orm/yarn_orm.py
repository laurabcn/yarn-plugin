from typing import Any

from sqlalchemy import ARRAY, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR, UUID
from sqlalchemy.orm import Mapped, mapped_column

from yarn_plugin.infrastructure.database import Base


class YarnModel(Base):
    __tablename__ = "yarns"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    brand_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("brands.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    weight: Mapped[str] = mapped_column(String(50), nullable=False)
    fiber_types: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    needle_min_mm: Mapped[float | None] = mapped_column(Float, nullable=True)
    needle_max_mm: Mapped[float | None] = mapped_column(Float, nullable=True)
    ball_weight_grams: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ball_length_meters: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gauge_stitches: Mapped[int] = mapped_column(Integer, nullable=False)
    gauge_rows: Mapped[int] = mapped_column(Integer, nullable=False)
    care_machine_washable: Mapped[bool] = mapped_column(Boolean, nullable=False)
    care_wash_temperature_celsius: Mapped[int | None] = mapped_column(Integer, nullable=True)
    care_wash_program: Mapped[str | None] = mapped_column(String(100), nullable=True)
    care_bleach_allowed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    care_tumble_dry_allowed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    care_dry_clean_allowed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    care_dry_flat: Mapped[bool] = mapped_column(Boolean, nullable=False)
    care_max_iron_temperature_celsius: Mapped[int | None] = mapped_column(Integer, nullable=True)
    crochet_hook_size_mm: Mapped[float | None] = mapped_column(Float, nullable=True)
    balls_per_garment: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, nullable=False, default=[])
    colors: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, nullable=False, default=[])
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=[])
    search_vector: Mapped[str | None] = mapped_column(TSVECTOR, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
