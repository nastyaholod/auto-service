from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.application.dto import CreateVehicleCommand, VehicleDTO
from app.infrastructure.uow import SqlAlchemyUnitOfWork
from app.presentation.api.deps import get_uow

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.post("", response_model=VehicleDTO, status_code=201)
async def create_vehicle(
    cmd: CreateVehicleCommand,
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
):
    from app.domain.entities import Vehicle
    try:
        vehicle = Vehicle.create(
            client_id=cmd.client_id,
            vin=cmd.vin,
            brand=cmd.brand,
            model=cmd.model,
            year=cmd.year,
            license_plate=cmd.license_plate,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    await uow.vehicle_repo.save(vehicle)
    await uow.commit()

    return VehicleDTO(
        id=vehicle.id,
        client_id=vehicle.client_id,
        vin=vehicle.vin.value,
        brand=vehicle.brand,
        model=vehicle.model,
        year=vehicle.year,
        license_plate=vehicle.license_plate.value,
    )


@router.get("/by-client/{client_id}", response_model=list[VehicleDTO])
async def list_vehicles_by_client(
    client_id: UUID,
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
):
    vehicles = await uow.vehicle_repo.list_by_client(client_id)
    return [
        VehicleDTO(
            id=v.id,
            client_id=v.client_id,
            vin=v.vin.value,
            brand=v.brand,
            model=v.model,
            year=v.year,
            license_plate=v.license_plate.value,
        )
        for v in vehicles
    ]