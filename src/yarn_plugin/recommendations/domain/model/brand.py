from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass
class Brand:
    name: str
    id: UUID = field(default_factory=uuid4)
    website: str | None = None
    description: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Brand name must not be empty")