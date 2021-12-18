from fastapi.middleware import Middleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.core.backend import oauth2_backend
from app.core.config import settings

# TODO: Implement AuthenticationMiddleware + AuthenticationBackend
middleware = [Middleware(AuthenticationMiddleware, backend=oauth2_backend)]


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


if settings.BACKEND_CORS_ORIGINS:
    middleware.append(
        Middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    )

if settings.ALLOWED_HOSTS:
    # Enforces that all incoming requests have a correctly set Host header,
    # in order to guard against HTTP Host Header attacks.
    middleware.append(
        Middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.ALLOWED_HOSTS,
        )
    )


if not settings.DEBUG:
    # Enforces that all incoming requests must either be https or wss.
    middleware.append(Middleware(HTTPSRedirectMiddleware))
