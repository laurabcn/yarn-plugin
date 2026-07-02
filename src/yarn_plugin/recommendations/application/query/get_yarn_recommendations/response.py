from dataclasses import dataclass
from uuid import UUID

from yarn_plugin.recommendations.domain.model.yarn_weight import YarnWeight


@dataclass(frozen=True)
class YarnDto:
    id: UUID
    name: str
    brand_id: UUID
    weight: YarnWeight
    fiber_content: str
    description: str | None
    tags: tuple[str, ...]


@dataclass(frozen=True)
class GetYarnRecommendationsResponse:
    results: tuple[YarnDto, ...]
    total: int
    message: str
