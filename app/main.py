from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from structlog import configure_once as configure_structlog

from app.api import api_router
from app.core.backends import oauth2_backend
from app.core.config import settings
from app.db.init import init_db
from app.packages.fastapi_versioning import VersionedFastAPI

app = FastAPI(title=settings.PROJECT_NAME)


app.include_router(api_router)


app = VersionedFastAPI(
    app=app,
    default_version=(0, 1),
    version_format="{major}.{minor}.{patch}",
    prefix_format="/v{major}",
    enable_latest=True,
    version=".".join([str(v) for v in settings.LATEST_VERSION]),
)


@app.on_event("startup")
async def on_startup():
    configure_structlog()
    await init_db()


app.add_middleware(AuthenticationMiddleware, backend=oauth2_backend)


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


if settings.ALLOWED_HOSTS:
    # Enforces that all incoming requests have a correctly set Host header,
    # in order to guard against HTTP Host Header attacks.
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS,
    )


if not settings.DEBUG:
    # Enforces that all incoming requests must either be https or wss.
    app.add_middleware(HTTPSRedirectMiddleware)


# TODO: Read about GZipMiddleware
# https://fastapi.tiangolo.com/advanced/middleware/#gzipmiddleware


# TODO: Integrate Sentry
# https://docs.sentry.io/platforms/python/guides/asgi/


# TODO: Read about ProxyHeadersMiddleware
# https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py


# TODO: Read about MessagePack
# https://github.com/florimondmanca/msgpack-asgi


# TODO: check other available middleware
# https://www.starlette.io/middleware/
# https://github.com/florimondmanca/msgpack-asgi
