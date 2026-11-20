from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.config import DatabaseConfig
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.application.dto import RegisterUserCommand, LoginUserCommand, TokenResponse, UserDTO
from app.application.use_cases.register_user import RegisterUserUseCase
from app.application.use_cases.login_user import LoginUserUseCase

router = APIRouter(prefix="/auth", tags=["auth"])

def get_session():
    config = DatabaseConfig()
    engine = create_async_engine(config.dsn)
    session_factory = async_sessionmaker(engine)
    return session_factory()

@router.post("/register", response_model=UserDTO, status_code=201)
async def register(cmd: RegisterUserCommand):
    session = get_session()
    try:
        use_case = RegisterUserUseCase(session)
        return await use_case.execute(cmd)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await session.close()

@router.post("/login", response_model=TokenResponse)
async def login(cmd: LoginUserCommand):
    session = get_session()
    try:
        use_case = LoginUserUseCase(session)
        return await use_case.execute(cmd)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    finally:
        await session.close()