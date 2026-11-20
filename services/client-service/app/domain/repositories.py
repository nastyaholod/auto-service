from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional, List

from app.domain.entities import Client, Vehicle


class ClientRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[Client]:
        ...

    @abstractmethod
    async def save(self, client: Client) -> None:
        ...


class VehicleRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[Vehicle]:
        ...

    @abstractmethod
    async def list_by_client(self, client_id: UUID) -> List[Vehicle]:
        ...

    @abstractmethod
    async def save(self, vehicle: Vehicle) -> None:
        ...