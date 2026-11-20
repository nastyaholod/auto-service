from pydantic import BaseModel, Field
from uuid import UUID

class WorkOrderLineDTO(BaseModel):
    part_id: UUID
    part_name: str
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)

class CreateWorkOrderCommand(BaseModel):
    vehicle_id: UUID
    lines: list[WorkOrderLineDTO]

class WorkOrderDTO(BaseModel):
    id: UUID
    vehicle_id: UUID
    status: str
    total_amount: float
    currency: str
    created_at: str