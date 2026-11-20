from app.application.dto import RegisterUserCommand, UserDTO
from app.domain.entities import User, UserRole
from app.infrastructure.security import hash_password
from app.infrastructure.database.models import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import uuid

class RegisterUserUseCase:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def execute(self, cmd: RegisterUserCommand) -> UserDTO:
        user_model = UserModel(
            id=uuid.uuid4(),
            email=cmd.email,
            hashed_password=hash_password(cmd.password),
            first_name=cmd.first_name,
            last_name=cmd.last_name,
            role=UserRole.CLIENT,
            is_active=True,
            created_at=datetime.utcnow()
        )
        self._session.add(user_model)
        await self._session.commit()
        await self._session.refresh(user_model)

        return UserDTO(
            id=user_model.id,
            email=user_model.email,
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            role=user_model.role.value,
            created_at=user_model.created_at
        )