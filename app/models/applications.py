from typing import List, Optional
from uuid import UUID, uuid4

from sqlmodel import Column, DateTime, Field, Relationship

from app.core.datetime import datetime
from app.core.security import check_password, get_password_hash
from app.packages.sqlmodel import SQLModel

__all__ = [
    "ApplicationBase",
    "ApplicationRead",
    "ApplicationCreate",
    "Application",
]


class ApplicationBase(SQLModel):
    client_id: str = Field(
        max_length=255,
        nullable=False,
        sa_column_kwargs=dict(unique=True),
    )


class ApplicationRead(ApplicationBase):
    pass


class Application(ApplicationBase, table=True):
    id: UUID = Field(
        primary_key=True,
        default_factory=uuid4,
        nullable=False,
        sa_column_kwargs=dict(unique=True),
    )
    user_id: Optional[UUID] = Field(foreign_key="user.id", nullable=True)
    client_secret: str = Field(max_length=255)
    redirect_uris: Optional[str] = Field(default="")
    # TODO: add choices: confidential, public
    # client_type: str = Field(max_length=32, default="confidential")
    # TODO: add choices
    # authorization_grant_type: str = Field(max_length=32, default="")
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)), default_factory=datetime.now
    )
    deactivated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True)), nullable=True
    )
    access_tokens: List["AccessToken"] = Relationship(back_populates="application")
    refresh_tokens: List["RefreshToken"] = Relationship(back_populates="application")
    # name
    # skip authorization
    # algorithm

    def __init__(self, client_secret: str, **kwargs) -> None:
        self.client_secret = self.get_secret_hash(client_secret)
        super().__init__(**kwargs)

    @property
    def is_active(self) -> bool:
        return bool(not self.deactivated_at)

    @staticmethod
    def get_secret_hash(client_secret: str) -> str:
        return get_password_hash(client_secret)

    def check_secret(self, client_secret: str) -> bool:
        return check_password(client_secret, self.client_secret)


class ApplicationCreate(ApplicationBase):
    client_secret: str
