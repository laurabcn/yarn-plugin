from dataclasses import dataclass

from yarn_plugin.recommendations.domain.model.sleeve_type import SleeveType


@dataclass(frozen=True)
class BallsRequirement:
    """Número de ovillos necesarios para tejer una prenda de una talla y tipo de manga concretos."""

    garment_size: str
    sleeve_type: SleeveType
    balls_needed: int

    def __post_init__(self) -> None:
        if not self.garment_size or not self.garment_size.strip():
            raise ValueError("Garment size must not be empty")
        if self.balls_needed <= 0:
            raise ValueError("Balls needed must be greater than zero")
