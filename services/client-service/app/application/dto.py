from pydantic import BaseModel, Field
from uuid import UUID


class CreateClientCommand(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    phone: str
    email: str


class ClientDTO(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    phone: str
    email: str


class CreateVehicleCommand(BaseModel):
    client_id: UUID
    vin: str
    brand: str
    model: str
    year: int = Field(ge=1886, le=2100)
    license_plate: str


class VehicleDTO(BaseModel):
    id: UUID
    client_id: UUID
    vin: str
    brand: str
    model: str
    year: int
    license_plate: str