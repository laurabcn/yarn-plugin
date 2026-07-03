from dataclasses import dataclass
from uuid import UUID

from yarn_plugin.recommendations.domain.model.ball_spec import BallSpec
from yarn_plugin.recommendations.domain.model.balls_requirement import BallsRequirement
from yarn_plugin.recommendations.domain.model.care_instructions import CareInstructions
from yarn_plugin.recommendations.domain.model.color import Color
from yarn_plugin.recommendations.domain.model.fiber_type import FiberType
from yarn_plugin.recommendations.domain.model.gauge import Gauge
from yarn_plugin.recommendations.domain.model.needle_size import NeedleSize
from yarn_plugin.recommendations.domain.model.yarn_weight import YarnWeight


@dataclass(frozen=True)
class YarnDto:
    id: UUID
    name: str
    brand_id: UUID
    weight: YarnWeight
    fiber_types: tuple[FiberType, ...]
    gauge: Gauge
    care_instructions: CareInstructions
    description: str | None
    needle_size: NeedleSize | None
    ball_spec: BallSpec | None
    crochet_hook_size_mm: float | None
    tags: tuple[str, ...]
    colors: tuple[Color, ...]
    balls_per_garment: tuple[BallsRequirement, ...]


@dataclass(frozen=True)
class GetYarnRecommendationsResponse:
    results: tuple[YarnDto, ...]
    total: int
    message: str
