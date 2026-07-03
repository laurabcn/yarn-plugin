from dataclasses import dataclass


@dataclass(frozen=True)
class Gauge:
    """Muestra de tensión: puntos y filas obtenidos en un cuadrado de 10x10cm."""

    stitches: int
    rows: int

    def __post_init__(self) -> None:
        if self.stitches <= 0:
            raise ValueError("Stitches must be greater than zero")
        if self.rows <= 0:
            raise ValueError("Rows must be greater than zero")
