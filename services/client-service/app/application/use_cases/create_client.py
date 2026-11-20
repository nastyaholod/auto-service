from app.application.dto import CreateClientCommand, ClientDTO
from app.application.interfaces import UnitOfWork
from app.domain.entities import Client


class CreateClientUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(self, cmd: CreateClientCommand) -> ClientDTO:
        client = Client.create(
            first_name=cmd.first_name,
            last_name=cmd.last_name,
            phone=cmd.phone,
            email=cmd.email,
        )
        await self._uow.client_repo.save(client)
        await self._uow.commit()
        return ClientDTO(
            id=client.id,
            first_name=client.first_name,
            last_name=client.last_name,
            phone=client.phone.value,
            email=client.email.value,
        )