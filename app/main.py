from fastapi import FastAPI
from structlog import configure_once as configure_structlog

from app.api import api_router
from app.core.config import settings
from app.core.middleware import middleware
from app.db.init import init_db
from app.packages.fastapi_versioning import VersionedFastAPI

app = FastAPI(
    title=settings.PROJECT_NAME,
    middleware=middleware,
)


app.include_router(api_router)


@app.on_event("startup")
async def on_startup():
    configure_structlog()
    await init_db()


# TODO: check why middlewares are not working
app = VersionedFastAPI(
    app=app,
    default_version=(0, 1),
    version_format="{major}.{minor}.{patch}",
    prefix_format="/v{major}",
    enable_latest=True,
    version=".".join([str(v) for v in settings.LATEST_VERSION]),
)
