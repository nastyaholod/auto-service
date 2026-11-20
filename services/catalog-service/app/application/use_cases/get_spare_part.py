from uuid import UUID
from app.application.dto import SparePartDTO
from app.application.interfaces import UnitOfWork
from app.infrastructure.cache.redis_cache import RedisCache

class GetSparePartUseCase:
    def __init__(self, uow: UnitOfWork, cache: RedisCache):
        self._uow = uow
        self._cache = cache

    async def execute(self, part_id: UUID) -> SparePartDTO:
        # 1. Проверяем кэш
        cached_part = await self._cache.get_spare_part(part_id)
        if cached_part:
            print(f"[CACHE HIT] Запчасть {part_id} получена из Redis")
            return cached_part

        # 2. Если нет в кэше, идем в БД
        print(f"[CACHE MISS] Запчасть {part_id} не найдена в Redis, запрос к БД")
        part = await self._uow.spare_part_repo.get_by_id(part_id)
        if part is None:
            raise ValueError("Spare part not found")

        dto = SparePartDTO(
            id=part.id,
            article_number=part.article_number,
            name=part.name,
            price_amount=part.price.amount,
            currency=part.price.currency,
            stock_quantity=part.stock_quantity
        )

        # 3. Сохраняем в кэш на 60 секунд
        await self._cache.set_spare_part(dto, ttl=60)
        return dto