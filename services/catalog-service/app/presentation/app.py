from contextlib import asynccontextmanager
from fastapi import FastAPI
import grpc
from concurrent import futures
import catalog_pb2_grpc

# Импортируем наш класс-обработчик gRPC
from app.infrastructure.grpc.server import CatalogServiceServicer

# Глобальная переменная для хранения ссылки на сервер
grpc_server = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global grpc_server
    print("[gRPC] Инициализация сервера...")
    
    # 1. Создаем и запускаем gRPC сервер при старте приложения
    grpc_server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    catalog_pb2_grpc.add_CatalogServiceServicer_to_server(
        CatalogServiceServicer(), grpc_server
    )
    grpc_server.add_insecure_port('[::]:50051')
    await grpc_server.start()
    print("[gRPC] ✅ Сервер успешно запущен и слушает порт 50051")
    
    yield  # <--- Здесь приложение работает и обрабатывает запросы
    
    # 2. Корректно останавливаем сервер при выключении
    print("[gRPC] Остановка сервера...")
    if grpc_server:
        await grpc_server.stop(grace=None)

def create_app() -> FastAPI:
    app = FastAPI(
        title="Catalog Service",
        version="0.1.0",
        description="Catalog bounded context with gRPC",
        lifespan=lifespan,  # <-- ПОДКЛЮЧАЕМ НАШ МЕНЕДЖЕР ЖИЗНЕННОГО ЦИКЛА
    )
    
    # Здесь должны быть ваши роутеры, например:
    from app.presentation.api.routers import spare_parts
    app.include_router(spare_parts.router, prefix="/api/v1")

    @app.get("/health")
    async def health():
        return {"status": "ok", "service": "catalog-service"}

    return app