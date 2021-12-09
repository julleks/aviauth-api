from fastapi import FastAPI
from app.core.config import settings
from app.api import api_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.LATEST_VERSION,
)

app.include_router(api_router)
