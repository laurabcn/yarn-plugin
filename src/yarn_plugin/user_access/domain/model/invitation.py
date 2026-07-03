from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID


@dataclass
class Invitation:
    id: UUID
    email: str
    token: str
    expires_at: datetime
    created_at: datetime
    accepted_at: datetime | None = field(default=None)

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) > self.expires_at.replace(tzinfo=timezone.utc)

    def is_used(self) -> bool:
        return self.accepted_at is not None

    def accept(self) -> None:
        self.accepted_at = datetime.now(timezone.utc)
