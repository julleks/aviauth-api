import os
from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = PostgresDsn.allowed_schemes
    allowed_schemes.add("postgresql+asyncpg")


class Settings(BaseSettings):
    PROJECT_NAME: str = "aviauth-api"
    VERSION: str = "0.1.0"

    DEBUG: bool = os.getenv("DEBUG", False)

    @validator("SQLALCHEMY_DATABASE_URL", pre=True)
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

    SQLALCHEMY_DATABASE_URL: Optional[PostgresDsn] = None


settings = Settings()
