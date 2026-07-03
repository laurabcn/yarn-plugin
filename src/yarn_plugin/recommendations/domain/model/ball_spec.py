from dataclasses import dataclass


@dataclass(frozen=True)
class BallSpec:
    """Peso y metraje de un ovillo, ej. 50g / 135m."""

    weight_grams: int
    length_meters: int

    def __post_init__(self) -> None:
        if self.weight_grams <= 0:
            raise ValueError("Weight must be greater than zero")
        if self.length_meters <= 0:
            raise ValueError("Length must be greater than zero")
