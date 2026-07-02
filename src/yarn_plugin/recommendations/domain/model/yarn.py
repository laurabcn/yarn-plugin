from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from yarn_plugin.recommendations.domain.model.yarn_weight import YarnWeight


@dataclass
class Yarn:
    brand_id: UUID
    name: str
    weight: YarnWeight
    fiber_content: str
    id: UUID = field(default_factory=uuid4)
    description: str | None = None
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Yarn name must not be empty")
        if not self.fiber_content or not self.fiber_content.strip():
            raise ValueError("Fiber content must not be empty")
