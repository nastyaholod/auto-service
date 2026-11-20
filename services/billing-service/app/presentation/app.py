from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI(
        title="Billing Service",
        version="0.1.0",
        description="Billing bounded context for Auto Service",
    )

    @app.get("/health")
    async def health():
        return {"status": "ok", "service": "billing-service"}

    return app