from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional

from app.domain.entities import SparePart
from app.domain.repositories import SparePartRepository
from app.domain.value_objects import Money
from app.infrastructure.database.models import SparePartModel

class SqlAlchemySparePartRepository(SparePartRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, id: UUID) -> Optional[SparePart]:
        result = await self._session.get(SparePartModel, id)
        if result is None:
            return None
        return self._to_domain(result)

    async def save(self, part: SparePart) -> None:
        model = SparePartModel(
            id=part.id,
            article_number=part.article_number,
            name=part.name,
            price_amount=part.price.amount,
            stock_quantity=part.stock_quantity
        )
        self._session.add(model)

    @staticmethod
    def _to_domain(model: SparePartModel) -> SparePart:
        return SparePart(
            id=model.id,
            article_number=model.article_number,
            name=model.name,
            price=Money(amount=float(model.price_amount)),
            stock_quantity=model.stock_quantity
        )