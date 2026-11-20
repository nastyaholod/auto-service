from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import uuid4
from datetime import datetime
import json

from app.domain.events import WorkOrderCreatedEvent
from app.infrastructure.database.models import OutboxEventModel

class OutboxRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save_work_order_created_event(self, event: WorkOrderCreatedEvent):
        outbox_event = OutboxEventModel(
            id=uuid4(),
            event_type="WorkOrderCreated",
            payload=json.dumps({
                "work_order_id": str(event.work_order_id),
                "vehicle_id": str(event.vehicle_id),
                "total_amount": event.total_amount,
                "created_at": event.created_at.isoformat()
            }),
            created_at=datetime.utcnow(),
            published=False
        )
        self._session.add(outbox_event)

    async def get_unpublished_events(self, limit: int = 10):
        result = await self._session.execute(
            select(OutboxEventModel)
            .where(OutboxEventModel.published == False)
            .limit(limit)
        )
        return result.scalars().all()

    async def mark_as_published(self, event_id):
        event = await self._session.get(OutboxEventModel, event_id)
        if event:
            event.published = True