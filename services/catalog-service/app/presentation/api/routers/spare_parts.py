from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.application.dto import CreateSparePartCommand, SparePartDTO
from app.application.use_cases.create_spare_part import CreateSparePartUseCase
from app.application.use_cases.get_spare_part import GetSparePartUseCase
from app.infrastructure.uow import SqlAlchemyUnitOfWork
from app.infrastructure.cache.redis_cache import RedisCache
from app.presentation.api.deps import get_uow, get_cache

router = APIRouter(prefix="/spare-parts", tags=["spare-parts"])

@router.post("", response_model=SparePartDTO, status_code=201)
async def create_spare_part(
    cmd: CreateSparePartCommand,
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
):
    use_case = CreateSparePartUseCase(uow)
    try:
        return await use_case.execute(cmd)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{part_id}", response_model=SparePartDTO)
async def get_spare_part(
    part_id: UUID,
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
    cache: RedisCache = Depends(get_cache),
):
    use_case = GetSparePartUseCase(uow, cache)
    try:
        return await use_case.execute(part_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))