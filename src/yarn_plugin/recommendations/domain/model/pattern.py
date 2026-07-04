from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from yarn_plugin.recommendations.domain.model.difficulty import Difficulty
from yarn_plugin.recommendations.domain.model.language import Language
from yarn_plugin.recommendations.domain.model.needle_size import NeedleSize
from yarn_plugin.recommendations.domain.model.pattern_category import PatternCategory
from yarn_plugin.recommendations.domain.model.yarn_weight import YarnWeight


@dataclass
class Pattern:
    brand_id: UUID
    name: str
    difficulty: Difficulty
    yarn_weight: YarnWeight
    category: PatternCategory
    language: Language
    needle_size: NeedleSize
    id: UUID = field(default_factory=uuid4)
    recommended_yarn_id: UUID | None = None
    popularity_rating: float | None = None
    description: str | None = None
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Pattern name must not be empty")
        if self.popularity_rating is not None and not (1.0 <= self.popularity_rating <= 5.0):
            raise ValueError("Popularity rating must be between 1 and 5")
