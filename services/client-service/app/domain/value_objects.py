from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", self.value):
            raise ValueError(f"Invalid email: {self.value}")


@dataclass(frozen=True)
class PhoneNumber:
    value: str

    def __post_init__(self):
        if not re.match(r"^\+?[0-9]{10,15}$", self.value):
            raise ValueError(f"Invalid phone: {self.value}")


@dataclass(frozen=True)
class Vin:
    value: str

    def __post_init__(self):
        if len(self.value) != 17 or not self.value.isalnum():
            raise ValueError(f"Invalid VIN: {self.value}")
        object.__setattr__(self, "value", self.value.upper())


@dataclass(frozen=True)
class LicensePlate:
    value: str

    def __post_init__(self):
        if not self.value or len(self.value) > 10:
            raise ValueError(f"Invalid license plate: {self.value}")
        object.__setattr__(self, "value", self.value.upper())