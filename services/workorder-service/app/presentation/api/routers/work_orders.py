from fastapi import APIRouter, Depends, HTTPException
import os

from app.application.dto import CreateWorkOrderCommand, WorkOrderDTO
from app.application.use_cases.create_work_order import CreateWorkOrderUseCase
from app.infrastructure.uow import SqlAlchemyUnitOfWork
from app.infrastructure.outbox.outbox_repository import OutboxRepository
from app.infrastructure.grpc.client import CatalogGrpcClient
from app.presentation.api.deps import get_uow, get_outbox_repo

router = APIRouter(prefix="/work-orders", tags=["work-orders"])

grpc_client = CatalogGrpcClient(
    host=os.getenv("CATALOG_GRPC_HOST", "catalog-service"),
    port=int(os.getenv("CATALOG_GRPC_PORT", 50051))
)

@router.post("", response_model=WorkOrderDTO, status_code=201)
async def create_work_order(
    cmd: CreateWorkOrderCommand,
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
    outbox_repo: OutboxRepository = Depends(get_outbox_repo),
):
    use_case = CreateWorkOrderUseCase(uow, outbox_repo, grpc_client)
    try:
        return await use_case.execute(cmd)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))