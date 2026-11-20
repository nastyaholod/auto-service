from sqlalchemy.ext.asyncio import AsyncSession
from app.application.interfaces import UnitOfWork
from app.domain.repositories import SparePartRepository
from app.infrastructure.repositories.sqlalchemy_spare_part_repository import SqlAlchemySparePartRepository

class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.spare_part_repo: SparePartRepository = SqlAlchemySparePartRepository(session)

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()