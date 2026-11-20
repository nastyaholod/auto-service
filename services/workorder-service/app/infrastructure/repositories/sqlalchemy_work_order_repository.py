from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional

from app.domain.entities import WorkOrder, WorkOrderLine
from app.domain.repositories import WorkOrderRepository
from app.domain.value_objects import Money, WorkOrderStatus
from app.infrastructure.database.models import WorkOrderModel, WorkOrderLineModel

class SqlAlchemyWorkOrderRepository(WorkOrderRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, id: UUID) -> Optional[WorkOrder]:
        result = await self._session.get(WorkOrderModel, id)
        if result is None:
            return None
        return self._to_domain(result)

    async def save(self, work_order: WorkOrder) -> None:
        model = WorkOrderModel(
            id=work_order.id,
            vehicle_id=work_order.vehicle_id,
            status=work_order.status,
            total_amount=work_order.total_amount.amount,
            created_at=work_order.created_at
        )
        
        for line in work_order.lines:
            line_model = WorkOrderLineModel(
                id=line.id,
                work_order_id=work_order.id,
                part_id=line.part_id,
                part_name=line.part_name,
                quantity=line.quantity,
                price_at_moment=line.price_at_moment.amount
            )
            model.lines.append(line_model)
        
        self._session.add(model)

    @staticmethod
    def _to_domain(model: WorkOrderModel) -> WorkOrder:
        lines = [
            WorkOrderLine(
                id=line.id,
                part_id=line.part_id,
                part_name=line.part_name,
                quantity=line.quantity,
                price_at_moment=Money(amount=float(line.price_at_moment))
            )
            for line in model.lines
        ]
        
        return WorkOrder(
            id=model.id,
            vehicle_id=model.vehicle_id,
            status=WorkOrderStatus(model.status),
            total_amount=Money(amount=float(model.total_amount)),
            lines=lines,
            created_at=model.created_at
        )