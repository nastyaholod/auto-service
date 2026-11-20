from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
import redis.asyncio as redis

from app.infrastructure.database.config import DatabaseConfig, RedisConfig
from app.infrastructure.uow import SqlAlchemyUnitOfWork
from app.infrastructure.cache.redis_cache import RedisCache

_db_config = DatabaseConfig()
_redis_config = RedisConfig()

_engine = create_async_engine(_db_config.dsn, echo=False)
_session_factory = async_sessionmaker(_engine, expire_on_commit=False)
_redis_client = redis.from_url(_redis_config.dsn, decode_responses=True)

async def get_session():
    async with _session_factory() as session:
        yield session

async def get_uow(session: AsyncSession = Depends(get_session)) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session)

async def get_cache() -> RedisCache:
    return RedisCache(_redis_client)