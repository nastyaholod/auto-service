from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces import UnitOfWork
from app.domain.repositories import ClientRepository, VehicleRepository
from app.infrastructure.repositories.sqlalchemy_client_repository import SqlAlchemyClientRepository
from app.infrastructure.repositories.sqlalchemy_vehicle_repository import SqlAlchemyVehicleRepository


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.client_repo: ClientRepository = SqlAlchemyClientRepository(session)
        self.vehicle_repo: VehicleRepository = SqlAlchemyVehicleRepository(session)

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()