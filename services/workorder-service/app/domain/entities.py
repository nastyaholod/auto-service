from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import datetime
from app.domain.value_objects import Money, WorkOrderStatus

@dataclass
class WorkOrderLine:
    id: UUID
    part_id: UUID
    part_name: str
    quantity: int
    price_at_moment: Money

@dataclass
class WorkOrder:
    id: UUID
    vehicle_id: UUID
    status: WorkOrderStatus
    total_amount: Money
    lines: list[WorkOrderLine] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

    @classmethod
    def create(cls, vehicle_id: UUID) -> "WorkOrder":
        return cls(
            id=uuid4(),
            vehicle_id=vehicle_id,
            status=WorkOrderStatus.DRAFT,
            total_amount=Money(amount=0.0)
        )

    def add_line(self, part_id: UUID, part_name: str, quantity: int, price: float):
        line = WorkOrderLine(
            id=uuid4(),
            part_id=part_id,
            part_name=part_name,
            quantity=quantity,
            price_at_moment=Money(amount=price)
        )
        self.lines.append(line)
        self.total_amount = Money(amount=self.total_amount.amount + (price * quantity))