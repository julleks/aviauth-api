import os
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = PostgresDsn.allowed_schemes
    allowed_schemes.add("postgresql+asyncpg")


class Settings(BaseSettings):
    PROJECT_NAME: str = "aviauth-api"

    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    HASH_ALGORITHM = "HS256"
    ACCESS_TOKEN_LIFETIME = 30 * 60
    REFRESH_TOKEN_LIFETIME = 10 * 60 * 60
    API_URL = "http://localhost:8000"
    TOKEN_PATH: str = "auth/token"
    TOKEN_URL: str = None

    @validator("TOKEN_URL", pre=True)
    def token_url(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if v:
            return v
        return f"{values.get('API_URL')}/latest/{values.get('TOKEN_PATH')}"

    V0_VERSION = (0, 1, 0)
    LATEST_VERSION = V0_VERSION

    OAUTH2_SCOPES = {
        "user:read": "Read access to Identity information.",
        "user:write": "Write access to Identity information.",
        "applications:read": "Read access to Applications list.",
        "applications:write": "Write access to Applications list.",
    }

    MAX_DB_CONNECTION_RETRIES = 5 * 60
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


settings = Settings()
