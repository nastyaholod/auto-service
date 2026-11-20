from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from app.infrastructure.database.config import DatabaseConfig
from app.infrastructure.database.models import Base
from app.presentation.api.routers import work_orders

_db_config = DatabaseConfig()
_engine = create_async_engine(_db_config.dsn, echo=False)

def create_app() -> FastAPI:
    app = FastAPI(
        title="Work Order Service",
        version="0.1.0",
        description="Work Order bounded context for Auto Service",
    )
    
    @app.on_event("startup")
    async def startup_event():
        async with _engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    app.include_router(work_orders.router, prefix="/api/v1")

    @app.get("/health")
    async def health():
        return {"status": "ok", "service": "workorder-service"}

    return app