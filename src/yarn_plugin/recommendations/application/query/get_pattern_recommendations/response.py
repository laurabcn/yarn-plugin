from dataclasses import dataclass
from uuid import UUID

from yarn_plugin.recommendations.domain.model.difficulty import Difficulty
from yarn_plugin.recommendations.domain.model.language import Language
from yarn_plugin.recommendations.domain.model.needle_size import NeedleSize
from yarn_plugin.recommendations.domain.model.pattern_category import PatternCategory
from yarn_plugin.recommendations.domain.model.yarn_weight import YarnWeight


@dataclass(frozen=True)
class PatternDto:
    id: UUID
    name: str
    brand_id: UUID
    difficulty: Difficulty
    yarn_weight: YarnWeight
    category: PatternCategory
    language: Language
    needle_size: NeedleSize
    recommended_yarn_id: UUID | None
    popularity_rating: float | None
    description: str | None
    tags: tuple[str, ...]


@dataclass(frozen=True)
class GetPatternRecommendationsResponse:
    results: tuple[PatternDto, ...]
    total: int
    message: str
