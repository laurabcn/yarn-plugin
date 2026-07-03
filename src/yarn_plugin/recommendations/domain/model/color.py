from dataclasses import dataclass


@dataclass(frozen=True)
class Color:
    code: str
    name: str | None = None

    def __post_init__(self) -> None:
        if not self.code or not self.code.strip():
            raise ValueError("Color code must not be empty")
