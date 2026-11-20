import uvicorn
from app.presentation.app import create_app

app = create_app()

if __name__ == "__main__":
    # Uvicorn теперь полностью контролирует процесс, включая lifespan
    uvicorn.run(app, host="0.0.0.0", port=8000)