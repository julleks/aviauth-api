import os
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = PostgresDsn.allowed_schemes
    allowed_schemes.add("postgresql+asyncpg")


class Settings(BaseSettings):
    PROJECT_NAME: str = "aviauth-api"

    V0_VERSION = (0, 1, 0)
    LATEST_VERSION = V0_VERSION

    MAX_DB_CONNECTION_RETRIES = 5 * 60
    DB_CONNECTION_RETRY_WAIT_SECONDS = 5

    DEBUG: bool = os.getenv("DEBUG", False)

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
