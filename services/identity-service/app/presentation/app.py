from fastapi import FastAPI
from app.presentation.api.routers import auth

def create_app() -> FastAPI:
    app = FastAPI(
        title="Identity Service",
        version="0.1.0",
        description="Authentication and authorization service"
    )
    app.include_router(auth.router)
    return app