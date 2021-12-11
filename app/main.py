from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from structlog import configure_once as configure_structlog

from app.api import api_router
from app.core.config import settings
from app.db.init import init_db
from app.packages.fastapi_versioning import VersionedFastAPI

app = FastAPI(
    title=settings.PROJECT_NAME,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
async def on_startup():
    configure_structlog()
    await init_db()


app.include_router(api_router)

# TODO: fix displaying version at http://127.0.0.1:8000/docs
app = VersionedFastAPI(app=app)
