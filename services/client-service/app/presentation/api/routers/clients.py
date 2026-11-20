from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.application.dto import CreateClientCommand, ClientDTO
from app.application.use_cases.create_client import CreateClientUseCase
from app.infrastructure.uow import SqlAlchemyUnitOfWork
from app.presentation.api.deps import get_uow

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("", response_model=ClientDTO, status_code=201)
async def create_client(
    cmd: CreateClientCommand,
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
):
    use_case = CreateClientUseCase(uow)
    try:
        return await use_case.execute(cmd)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{client_id}", response_model=ClientDTO)
async def get_client(
    client_id: UUID,
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
):
    client = await uow.client_repo.get_by_id(client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return ClientDTO(
        id=client.id,
        first_name=client.first_name,
        last_name=client.last_name,
        phone=client.phone.value,
        email=client.email.value,
    )