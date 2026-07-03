from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from yarn_plugin.recommendations.domain.model.ball_spec import BallSpec
from yarn_plugin.recommendations.domain.model.balls_requirement import BallsRequirement
from yarn_plugin.recommendations.domain.model.care_instructions import CareInstructions
from yarn_plugin.recommendations.domain.model.color import Color
from yarn_plugin.recommendations.domain.model.fiber_type import FiberType
from yarn_plugin.recommendations.domain.model.gauge import Gauge
from yarn_plugin.recommendations.domain.model.needle_size import NeedleSize
from yarn_plugin.recommendations.domain.model.yarn_weight import YarnWeight


@dataclass
class Yarn:
    brand_id: UUID
    name: str
    weight: YarnWeight
    fiber_types: list[FiberType]
    gauge: Gauge
    care_instructions: CareInstructions
    id: UUID = field(default_factory=uuid4)
    description: str | None = None
    needle_size: NeedleSize | None = None
    ball_spec: BallSpec | None = None
    crochet_hook_size_mm: float | None = None
    tags: list[str] = field(default_factory=list)
    colors: list[Color] = field(default_factory=list)
    balls_per_garment: list[BallsRequirement] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Yarn name must not be empty")
        if not self.fiber_types:
            raise ValueError("Yarn must have at least one fiber type")
        if self.crochet_hook_size_mm is not None and self.crochet_hook_size_mm <= 0:
            raise ValueError("Crochet hook size must be greater than zero")
