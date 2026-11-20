from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class WorkOrderCreatedEvent:
    work_order_id: UUID
    vehicle_id: UUID
    total_amount: float
    created_at: datetime