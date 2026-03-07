from fastapi import FastAPI

from src.api.v1.endpoints import predict
from src.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(predict.router, prefix="/api/v1", tags=["Forecasting"])


@app.get("/")
async def root():
    return {"message": f"Bem-vindo ao {settings.PROJECT_NAME} API"}
