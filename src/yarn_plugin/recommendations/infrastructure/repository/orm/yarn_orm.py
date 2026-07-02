from sqlalchemy import ARRAY, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import TSVECTOR, UUID
from sqlalchemy.orm import Mapped, mapped_column

from yarn_plugin.infrastructure.database import Base


class YarnModel(Base):
    __tablename__ = "yarns"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    brand_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("brands.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    weight: Mapped[str] = mapped_column(String(50), nullable=False)
    fiber_content: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=[])
    search_vector: Mapped[str | None] = mapped_column(TSVECTOR, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)