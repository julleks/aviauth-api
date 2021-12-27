from typing import Optional
from uuid import UUID

from sqlmodel import Field

from app.core.datetime import datetime
from app.core.security import get_password_hash, verify_password
from app.packages.sqlmodel import SQLModel

__all__ = [
    "ApplicationBase",
    "ApplicationRead",
    "ApplicationCreate",
    "Application",
]


class ApplicationBase(SQLModel):
    client_id: str = Field(
        primary_key=True,
        max_length=255,
        nullable=False,
        sa_column_kwargs=dict(unique=True),
    )


class ApplicationRead(ApplicationBase):
    pass


class Application(ApplicationBase, table=True):
    user_id: Optional[UUID] = Field(foreign_key="user.id", nullable=True)
    client_secret: str = Field(max_length=255)
    redirect_uris: Optional[str] = Field(default="")
    # TODO: add choices: confidential, public
    # client_type: str = Field(max_length=32, default="confidential")
    # TODO: add choices
    # authorization_grant_type: str = Field(max_length=32, default="")
    created_at: datetime
    updated_at: datetime = Field(nullable=True)
    # name
    # skip authorization
    # algorithm

    def __init__(self, client_secret, **kwargs):
        self.created_at = datetime.now()
        self.client_secret = self.get_secret_hash(client_secret)
        super().__init__(**kwargs)

    @staticmethod
    def get_secret_hash(client_secret):
        return get_password_hash(client_secret)

    def verify_secret(self, client_secret):
        return verify_password(client_secret, self.client_secret)


class ApplicationCreate(ApplicationBase):
    client_secret: str
