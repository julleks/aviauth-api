from fastapi import FastAPI
from structlog import configure_once as configure_structlog

from app.api import api_router
from app.core.config import settings
from app.db.init import init_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)


@app.on_event("startup")
async def on_startup():
    configure_structlog()

    await init_db()


app.include_router(api_router)
