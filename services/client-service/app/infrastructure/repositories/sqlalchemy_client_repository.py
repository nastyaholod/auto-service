from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional

from app.domain.entities import Client
from app.domain.repositories import ClientRepository
from app.domain.value_objects import Email, PhoneNumber
from app.infrastructure.database.models import ClientModel


class SqlAlchemyClientRepository(ClientRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, id: UUID) -> Optional[Client]:
        result = await self._session.get(ClientModel, id)
        if result is None:
            return None
        return self._to_domain(result)

    async def save(self, client: Client) -> None:
        model = ClientModel(
            id=client.id,
            first_name=client.first_name,
            last_name=client.last_name,
            phone=client.phone.value,
            email=client.email.value,
            created_at=client.created_at,
        )
        self._session.add(model)

    @staticmethod
    def _to_domain(model: ClientModel) -> Client:
        return Client(
            id=model.id,
            first_name=model.first_name,
            last_name=model.last_name,
            phone=PhoneNumber(model.phone),
            email=Email(model.email),
            created_at=model.created_at,
        )