from sqlalchemy.ext.asyncio import AsyncSession
from app.application.interfaces import UnitOfWork
from app.domain.repositories import WorkOrderRepository
from app.infrastructure.repositories.sqlalchemy_work_order_repository import SqlAlchemyWorkOrderRepository

class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.work_order_repo: WorkOrderRepository = SqlAlchemyWorkOrderRepository(session)

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()