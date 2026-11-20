from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from app.domain.entities import SparePart

class SparePartRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[SparePart]:
        ...

    @abstractmethod
    async def save(self, part: SparePart) -> None:
        ...