from app.application.dto import CreateWorkOrderCommand, WorkOrderDTO
from app.application.interfaces import UnitOfWork
from app.domain.entities import WorkOrder
from app.domain.events import WorkOrderCreatedEvent
from app.infrastructure.outbox.outbox_repository import OutboxRepository
from app.infrastructure.grpc.client import CatalogGrpcClient

class CreateWorkOrderUseCase:
    def __init__(self, uow: UnitOfWork, outbox_repo: OutboxRepository, grpc_client: CatalogGrpcClient):
        self._uow = uow
        self._outbox_repo = outbox_repo
        self._grpc_client = grpc_client

    async def execute(self, cmd: CreateWorkOrderCommand) -> WorkOrderDTO:
        # 1. ПРОВЕРКА ЧЕРЕЗ gRPC
        for line in cmd.lines:
            is_available, message = await self._grpc_client.check_stock(str(line.part_id), line.quantity)
            if not is_available:
                raise ValueError(f"Ошибка резервирования: {message}")

        # 2. Создаем заказ-наряд
        work_order = WorkOrder.create(vehicle_id=cmd.vehicle_id)
        for line_cmd in cmd.lines:
            work_order.add_line(
                part_id=line_cmd.part_id,
                part_name=line_cmd.part_name,
                quantity=line_cmd.quantity,
                price=line_cmd.price
            )
        
        await self._uow.work_order_repo.save(work_order)
        
        event = WorkOrderCreatedEvent(
            work_order_id=work_order.id,
            vehicle_id=work_order.vehicle_id,
            total_amount=work_order.total_amount.amount,
            created_at=work_order.created_at
        )
        await self._outbox_repo.save_work_order_created_event(event)
        await self._uow.commit()
        
        return WorkOrderDTO(
            id=work_order.id,
            vehicle_id=work_order.vehicle_id,
            status=work_order.status.value,
            total_amount=work_order.total_amount.amount,
            currency=work_order.total_amount.currency,
            created_at=work_order.created_at.isoformat()
        )