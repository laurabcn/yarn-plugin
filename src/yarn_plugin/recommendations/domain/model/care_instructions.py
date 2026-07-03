from dataclasses import dataclass


@dataclass(frozen=True)
class CareInstructions:
    """Instrucciones de lavado y cuidado de la etiqueta del ovillo."""

    machine_washable: bool
    wash_temperature_celsius: int | None
    wash_program: str | None
    bleach_allowed: bool
    tumble_dry_allowed: bool
    dry_clean_allowed: bool
    dry_flat: bool
    max_iron_temperature_celsius: int | None

    def __post_init__(self) -> None:
        if self.wash_temperature_celsius is not None and self.wash_temperature_celsius <= 0:
            raise ValueError("Wash temperature must be greater than zero")
        if self.max_iron_temperature_celsius is not None and self.max_iron_temperature_celsius <= 0:
            raise ValueError("Max iron temperature must be greater than zero")
