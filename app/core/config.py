from pydantic import BaseSettings, PostgresDsn, validator
from typing import Optional, Dict, Any
import os


class Settings(BaseSettings):
    PROJECT_NAME: str = "aviauth-api"
    LATEST_VERSION: str = "0.1.0"

    @classmethod
    @validator("SQLALCHEMY_DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=values.get('POSTGRES_DB'),
        )

    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "127.0.0.1")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "aviauth")

    SQLALCHEMY_DATABASE_URL: Optional[PostgresDsn] = None


settings = Settings()
