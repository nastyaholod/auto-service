import uvicorn
from app.presentation.app import create_app
from app.infrastructure.database.models import Base
from app.infrastructure.database.config import DatabaseConfig
from sqlalchemy.ext.asyncio import create_async_engine

app = create_app()

@app.on_event("startup")
async def startup():
    config = DatabaseConfig()
    engine = create_async_engine(config.dsn)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)