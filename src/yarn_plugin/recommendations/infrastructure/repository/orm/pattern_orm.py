from sqlalchemy import ARRAY, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import TSVECTOR, UUID
from sqlalchemy.orm import Mapped, mapped_column

from yarn_plugin.infrastructure.database import Base


class PatternModel(Base):
    __tablename__ = "patterns"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    brand_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("brands.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    difficulty: Mapped[str] = mapped_column(String(50), nullable=False)
    yarn_weight: Mapped[str] = mapped_column(String(50), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    language: Mapped[str] = mapped_column(String(10), nullable=False)
    needle_min_mm: Mapped[float] = mapped_column(Float, nullable=False)
    needle_max_mm: Mapped[float] = mapped_column(Float, nullable=False)
    recommended_yarn_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("yarns.id"), nullable=True
    )
    popularity_rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=[])
    search_vector: Mapped[str | None] = mapped_column(TSVECTOR, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
