from app.application.dto import LoginUserCommand, TokenResponse
from app.infrastructure.security import verify_password, create_access_token, create_refresh_token
from app.infrastructure.database.models import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class LoginUserUseCase:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def execute(self, cmd: LoginUserCommand) -> TokenResponse:
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == cmd.email)
        )
        user = result.scalar_one_or_none()

        if not user or not verify_password(cmd.password, user.hashed_password):
            raise ValueError("Неверный email или пароль")

        if not user.is_active:
            raise ValueError("Пользователь заблокирован")

        token_data = {"sub": str(user.id), "email": user.email, "role": user.role.value}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )