from abc import ABC, abstractmethod
from app.domain.repositories import ClientRepository, VehicleRepository


class UnitOfWork(ABC):
    client_repo: ClientRepository
    vehicle_repo: VehicleRepository

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...