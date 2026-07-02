from dataclasses import dataclass


@dataclass(frozen=True)
class NonEmptyStringValue:
    _value: str

    def __post_init__(self) -> None:
        if not self._value or not self._value.strip():
            raise ValueError("Value must not be empty")

    def value(self) -> str:
        return self._value
