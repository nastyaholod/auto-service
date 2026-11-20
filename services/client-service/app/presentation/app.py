from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from app.infrastructure.database.config import DatabaseConfig
from app.infrastructure.database.models import create_tables
from app.presentation.api.routers import clients, vehicles

_config = DatabaseConfig()
_engine = create_async_engine(_config.dsn, echo=False)

def create_app() -> FastAPI:
    app = FastAPI(
        title="Client Service",
        version="0.1.0",
        description="CRM bounded context for Auto Service",
    )
    
    @app.on_event("startup")
    async def startup_event():
        await create_tables(_engine)
    
    app.include_router(clients.router, prefix="/api/v1")
    app.include_router(vehicles.router, prefix="/api/v1")

    @app.get("/health")
    async def health():
        return {"status": "ok", "service": "client-service"}

    return app