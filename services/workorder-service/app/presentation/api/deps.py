from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.infrastructure.database.config import DatabaseConfig
from app.infrastructure.uow import SqlAlchemyUnitOfWork
from app.infrastructure.outbox.outbox_repository import OutboxRepository

_db_config = DatabaseConfig()
_engine = create_async_engine(_db_config.dsn, echo=False)
_session_factory = async_sessionmaker(_engine, expire_on_commit=False)

async def get_session():
    async with _session_factory() as session:
        yield session

async def get_uow(session: AsyncSession = Depends(get_session)) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session)

async def get_outbox_repo(session: AsyncSession = Depends(get_session)) -> OutboxRepository:
    return OutboxRepository(session)