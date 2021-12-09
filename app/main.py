from fastapi import FastAPI

from app.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.LATEST_VERSION,
)

app.include_router(api_router)
