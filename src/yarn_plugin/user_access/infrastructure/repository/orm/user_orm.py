import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from yarn_plugin.infrastructure.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    invitation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("invitations.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)