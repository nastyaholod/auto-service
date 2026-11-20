import grpc
from concurrent import futures
from uuid import UUID
import catalog_pb2
import catalog_pb2_grpc

from app.infrastructure.database.config import DatabaseConfig
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from app.infrastructure.database.models import SparePartModel

class CatalogServiceServicer(catalog_pb2_grpc.CatalogServiceServicer):
    def __init__(self):
        db_config = DatabaseConfig()
        self._engine = create_async_engine(db_config.dsn)
        self._session_factory = async_sessionmaker(self._engine, expire_on_commit=False)

    async def CheckStock(self, request, context):
        part_id = UUID(request.part_id)
        quantity = request.quantity
        
        async with self._session_factory() as session:
            result = await session.execute(
                select(SparePartModel).where(SparePartModel.id == part_id)
            )
            part = result.scalar_one_or_none()
            
            if not part:
                return catalog_pb2.CheckStockResponse(
                    is_available=False,
                    message=f"Запчасть {part_id} не найдена"
                )
            
            if part.stock_quantity >= quantity:
                return catalog_pb2.CheckStockResponse(
                    is_available=True,
                    message=f"Доступно {part.stock_quantity} шт."
                )
            else:
                return catalog_pb2.CheckStockResponse(
                    is_available=False,
                    message=f"Недостаточно на складе. Есть: {part.stock_quantity}, нужно: {quantity}"
                )

def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    catalog_pb2_grpc.add_CatalogServiceServicer_to_server(
        CatalogServiceServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    return server