from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import Optional, List

from app.domain.entities import Vehicle
from app.domain.repositories import VehicleRepository
from app.domain.value_objects import Vin, LicensePlate
from app.infrastructure.database.models import VehicleModel


class SqlAlchemyVehicleRepository(VehicleRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, id: UUID) -> Optional[Vehicle]:
        result = await self._session.get(VehicleModel, id)
        if result is None:
            return None
        return self._to_domain(result)

    async def list_by_client(self, client_id: UUID) -> List[Vehicle]:
        result = await self._session.execute(
            select(VehicleModel).where(VehicleModel.client_id == client_id)
        )
        return [self._to_domain(m) for m in result.scalars().all()]

    async def save(self, vehicle: Vehicle) -> None:
        model = VehicleModel(
            id=vehicle.id,
            client_id=vehicle.client_id,
            vin=vehicle.vin.value,
            brand=vehicle.brand,
            model=vehicle.model,
            year=vehicle.year,
            license_plate=vehicle.license_plate.value,
        )
        self._session.add(model)

    @staticmethod
    def _to_domain(model: VehicleModel) -> Vehicle:
        return Vehicle(
            id=model.id,
            client_id=model.client_id,
            vin=Vin(model.vin),
            brand=model.brand,
            model=model.model,
            year=model.year,
            license_plate=LicensePlate(model.license_plate),
        )