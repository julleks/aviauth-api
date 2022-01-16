import os
from functools import lru_cache
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator

__all__ = ["settings", "get_settings"]


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = PostgresDsn.allowed_schemes
    allowed_schemes.add("postgresql+asyncpg")


class SendgridSettings:
    API_KEY = os.getenv("SENDGRID_API_KEY")
    REGISTRATION_TPL = "d-977239e8c4bc4164800a05976bdfd1ba"


class EmailSettings:
    NO_REPLY_EMAIL = "no-reply@julleks.com"
    NO_REPLY_NAME = "Aviauth"


class Settings(BaseSettings):
    PROJECT_NAME: str = "aviauth-api"
    V0_VERSION = (0, 2, 0)
    LATEST_VERSION = V0_VERSION

    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", "41bfc53f79978dc3c758b5948aa5a2b9848c96eb485333e3003e1f7ea1c52296"
    )

    TOKEN_HASH_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_LIFETIME: int = 30 * 60
    REFRESH_TOKEN_LIFETIME: int = 10 * 60 * 60

    API_URL: str = "http://localhost:8000/latest"
    TOKEN_PATH: str = "auth/token"
    AUTHORIZATION_PATH: str = "auth/token"
    TOKEN_URL: str = None

    @validator("TOKEN_URL", pre=True)
    def token_url(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if v:
            return v
        return f"{values.get('API_URL')}/{values.get('TOKEN_PATH')}"

    OAUTH2_SCOPES = {
        "offline_access": "This scope requests an OAuth 2.0 Refresh Token be issued"
        "that can be used to obtain an Access Token that grants access"
        "to the End-User's UserInfo Endpoint even when the End-User is not present"
        "(not logged in).",
        "openid": "",
        "user:read": "Read access to Identity information.",
        "user:update": "Write access to Identity information.",
        "user:full": "Full access to Identity information.",
        "applications:read": "Read access to Applications list.",
        "applications:create": "Create access to Applications list.",
        "applications:update": "Update access to Applications list.",
        "applications:full": "Full access to Applications list.",
    }

    MAX_DB_CONNECTION_RETRIES = 5 * 60  # time in seconds
    DB_CONNECTION_RETRY_WAIT_SECONDS = 5

    DEBUG: bool = os.getenv("DEBUG", False)

    USE_TZ: bool = True

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # https://fastapi.tiangolo.com/tutorial/cors/
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # A list of domain names that should be allowed as hostnames.
    # Wildcard domains such as *.example.com are supported for matching subdomains
    # to allow any hostname either use allowed_hosts=["*"].
    ALLOWED_HOSTS: List[str] = []

    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return AsyncPostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB')}",
        )

    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "127.0.0.1")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "aviauth")

    DATABASE_URL: Optional[AsyncPostgresDsn] = None

    SENDGRID = SendgridSettings()
    EMAIL = EmailSettings()


@lru_cache()
def get_settings():
    return Settings()


# https://fastapi.tiangolo.com/advanced/settings/?h=settings#settings-in-a-dependency
settings = get_settings()
