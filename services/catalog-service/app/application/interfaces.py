from abc import ABC, abstractmethod
from app.domain.repositories import SparePartRepository

class UnitOfWork(ABC):
    spare_part_repo: SparePartRepository

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...