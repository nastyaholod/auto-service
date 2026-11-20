import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.application.use_cases.register_user import RegisterUserUseCase
from app.application.use_cases.login_user import LoginUserUseCase
from app.application.dto import RegisterUserCommand, LoginUserCommand
from app.domain.entities import UserRole
from app.infrastructure.security import hash_password
from uuid import uuid4
from datetime import datetime

class TestRegisterUserUseCase:
    @pytest.mark.asyncio
    async def test_register_user_success(self):
        # Arrange
        # Базовый мок сессии
        mock_session = MagicMock() 
        
        cmd = RegisterUserCommand(
            email="test@example.com",
            password="SecurePass123!",
            first_name="Тест",
            last_name="Тестов"
        )
        
        # Создаем мок-объект пользователя
        mock_user_instance = MagicMock()
        mock_user_instance.id = uuid4()
        mock_user_instance.email = cmd.email
        mock_user_instance.first_name = cmd.first_name
        mock_user_instance.last_name = cmd.last_name
        mock_user_instance.role = UserRole.CLIENT
        mock_user_instance.created_at = datetime.utcnow()

        # Явно задаем типы моков для методов сессии SQLAlchemy 2.0
        mock_session.add = MagicMock()          # Синхронный метод
        mock_session.commit = AsyncMock()       # Асинхронный метод
        mock_session.refresh = AsyncMock()      # Асинхронный метод

        # Патчим UserModel
        with patch('app.application.use_cases.register_user.UserModel', return_value=mock_user_instance):
            use_case = RegisterUserUseCase(mock_session)
            
            # Act
            result = await use_case.execute(cmd)
            
            # Assert
            assert result.email == cmd.email
            assert result.first_name == cmd.first_name
            assert result.last_name == cmd.last_name
            assert result.role == "CLIENT"
            
            # Проверяем вызовы
            mock_session.add.assert_called_once()
            mock_session.commit.assert_awaited_once()
            mock_session.refresh.assert_awaited_once()


class TestLoginUserUseCase:
    @pytest.mark.asyncio
    async def test_login_user_success(self):
        mock_session = AsyncMock()
        cmd = LoginUserCommand(email="test@example.com", password="SecurePass123!")
        
        mock_user = MagicMock()
        mock_user.email = cmd.email
        mock_user.hashed_password = hash_password(cmd.password)
        mock_user.is_active = True
        mock_user.id = uuid4()
        mock_user.role = UserRole.CLIENT
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_session.execute = AsyncMock(return_value=mock_result)
        
        use_case = LoginUserUseCase(mock_session)
        result = await use_case.execute(cmd)
        
        assert result.access_token is not None
        assert result.refresh_token is not None
        assert result.token_type == "bearer"

    @pytest.mark.asyncio
    async def test_login_user_wrong_password(self):
        mock_session = AsyncMock()
        cmd = LoginUserCommand(email="test@example.com", password="WrongPassword!")
        
        mock_user = MagicMock()
        mock_user.email = cmd.email
        mock_user.hashed_password = hash_password("CorrectPassword123!")
        mock_user.is_active = True
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_session.execute = AsyncMock(return_value=mock_result)
        
        use_case = LoginUserUseCase(mock_session)
        
        with pytest.raises(ValueError, match="Неверный email или пароль"):
            await use_case.execute(cmd)