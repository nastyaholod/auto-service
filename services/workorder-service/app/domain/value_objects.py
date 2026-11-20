from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "RUB"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")

class WorkOrderStatus(str, Enum):
    DRAFT = "DRAFT"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CLOSED = "CLOSED"