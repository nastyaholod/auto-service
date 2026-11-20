import json
from uuid import UUID
from typing import Optional
import redis.asyncio as redis

from app.application.dto import SparePartDTO

class RedisCache:
    def __init__(self, redis_client: redis.Redis):
        self._redis = redis_client

    async def get_spare_part(self, part_id: UUID) -> Optional[SparePartDTO]:
        key = f"spare_part:{part_id}"
        data = await self._redis.get(key)
        if data:
            return SparePartDTO.model_validate_json(data)
        return None

    async def set_spare_part(self, part: SparePartDTO, ttl: int = 60):
        key = f"spare_part:{part.id}"
        await self._redis.setex(key, ttl, part.model_dump_json())