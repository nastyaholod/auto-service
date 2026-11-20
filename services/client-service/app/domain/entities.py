from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import datetime

from app.domain.value_objects import Email, PhoneNumber, Vin, LicensePlate


@dataclass
class Client:
    id: UUID
    first_name: str
    last_name: str
    phone: PhoneNumber
    email: Email
    created_at: datetime = field(default_factory=datetime.utcnow)

    @classmethod
    def create(cls, first_name: str, last_name: str, phone: str, email: str) -> "Client":
        return cls(
            id=uuid4(),
            first_name=first_name,
            last_name=last_name,
            phone=PhoneNumber(phone),
            email=Email(email),
        )

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


@dataclass
class Vehicle:
    id: UUID
    client_id: UUID
    vin: Vin
    brand: str
    model: str
    year: int
    license_plate: LicensePlate

    @classmethod
    def create(
        cls,
        client_id: UUID,
        vin: str,
        brand: str,
        model: str,
        year: int,
        license_plate: str,
    ) -> "Vehicle":
        if year < 1886 or year > datetime.utcnow().year + 1:
            raise ValueError(f"Invalid year: {year}")
        return cls(
            id=uuid4(),
            client_id=client_id,
            vin=Vin(vin),
            brand=brand,
            model=model,
            year=year,
            license_plate=LicensePlate(license_plate),
        )