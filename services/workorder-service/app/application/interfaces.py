from abc import ABC, abstractmethod
from app.domain.repositories import WorkOrderRepository

class UnitOfWork(ABC):
    work_order_repo: WorkOrderRepository

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...