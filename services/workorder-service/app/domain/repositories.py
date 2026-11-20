from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from app.domain.entities import WorkOrder

class WorkOrderRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[WorkOrder]:
        ...

    @abstractmethod
    async def save(self, work_order: WorkOrder) -> None:
        ...