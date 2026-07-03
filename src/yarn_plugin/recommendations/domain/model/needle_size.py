from dataclasses import dataclass


@dataclass(frozen=True)
class NeedleSize:
    """Rango de agujas recomendado para tejer la lana, ej. de 2mm a 3mm."""

    min_mm: float
    max_mm: float

    def __post_init__(self) -> None:
        if self.min_mm <= 0:
            raise ValueError("Minimum needle size must be greater than zero")
        if self.max_mm <= 0:
            raise ValueError("Maximum needle size must be greater than zero")
        if self.min_mm > self.max_mm:
            raise ValueError("Minimum needle size must not exceed maximum needle size")
