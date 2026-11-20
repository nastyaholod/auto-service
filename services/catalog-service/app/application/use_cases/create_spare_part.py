from app.application.dto import CreateSparePartCommand, SparePartDTO
from app.application.interfaces import UnitOfWork
from app.domain.entities import SparePart

class CreateSparePartUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(self, cmd: CreateSparePartCommand) -> SparePartDTO:
        part = SparePart.create(
            article_number=cmd.article_number,
            name=cmd.name,
            price_amount=cmd.price_amount,
            stock_quantity=cmd.stock_quantity
        )
        await self._uow.spare_part_repo.save(part)
        await self._uow.commit()
        
        return SparePartDTO(
            id=part.id,
            article_number=part.article_number,
            name=part.name,
            price_amount=part.price.amount,
            currency=part.price.currency,
            stock_quantity=part.stock_quantity
        )