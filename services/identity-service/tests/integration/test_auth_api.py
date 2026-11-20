import pytest
from httpx import AsyncClient, ASGITransport
from app.presentation.app import create_app
from app.infrastructure.database.models import Base
from app.infrastructure.database.config import DatabaseConfig
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

@pytest.fixture
async def test_db():
    # Создаем тестовую БД (используем ту же, но очищаем таблицы)
    config = DatabaseConfig()
    engine = create_async_engine(config.dsn)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client(test_db):
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_register_and_login(client):
    # Регистрация
    register_data = {
        "email": "integration@test.com",
        "password": "TestPass123!",
        "first_name": "Интеграционный",
        "last_name": "Тест"
    }
    
    response = await client.post("/auth/register", json=register_data)
    assert response.status_code == 201
    
    user_data = response.json()
    assert user_data["email"] == register_data["email"]
    assert user_data["first_name"] == register_data["first_name"]
    assert user_data["role"] == "CLIENT"
    
    # Логин
    login_data = {
        "email": "integration@test.com",
        "password": "TestPass123!"
    }
    
    response = await client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    
    token_data = response.json()
    assert "access_token" in token_data
    assert "refresh_token" in token_data
    assert token_data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    # Первая регистрация
    register_data = {
        "email": "duplicate@test.com",
        "password": "TestPass123!",
        "first_name": "Первый",
        "last_name": "Пользователь"
    }
    
    response = await client.post("/auth/register", json=register_data)
    assert response.status_code == 201
    
    # Вторая регистрация с тем же email
    response = await client.post("/auth/register", json=register_data)
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_login_wrong_password(client):
    # Регистрация
    register_data = {
        "email": "wrongpass@test.com",
        "password": "CorrectPass123!",
        "first_name": "Тест",
        "last_name": "Тестов"
    }
    
    await client.post("/auth/register", json=register_data)
    
    # Логин с неправильным паролем
    login_data = {
        "email": "wrongpass@test.com",
        "password": "WrongPass123!"
    }
    
    response = await client.post("/auth/login", json=login_data)
    assert response.status_code == 401