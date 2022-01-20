from typing import List, Optional
from uuid import UUID, uuid4

from sqlmodel import Column, DateTime, Field, Relationship

from app.core.datetime import datetime
from app.core.security import get_password_hash, verify_password
from app.packages.sqlmodel import SQLModel

__all__ = [
    "UserBase",
    "UserRead",
    "UserCreate",
    "User",
]


class UserBase(SQLModel):
    email: str = Field(max_length=64, sa_column_kwargs={"unique": True})

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.email

    @staticmethod
    def get_password_hash(password):
        return get_password_hash(password)


class UserRead(UserBase):
    id: UUID = Field(
        primary_key=True,
        default_factory=uuid4,
        nullable=False,
        sa_column_kwargs=dict(unique=True),
    )
    username: Optional[str] = Field(
        max_length=64, sa_column_kwargs={"unique": True}, nullable=True
    )
    first_name: Optional[str] = Field(max_length=64, default="", nullable=False)
    last_name: Optional[str] = Field(max_length=64, default="", nullable=False)


class User(UserRead, table=True):
    password: str = Field(max_length=255, index=False, nullable=True)
    registered_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True)), default_factory=datetime.now
    )
    deactivated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True)), nullable=False
    )
    access_tokens: Optional[List["AccessToken"]] = Relationship(back_populates="user")
    refresh_tokens: Optional[List["RefreshToken"]] = Relationship(back_populates="user")

    @property
    def is_active(self) -> bool:
        return bool(not self.deactivated_at)

    def verify_password(self, password: str) -> bool:
        return verify_password(password, self.password)


class UserCreate(UserBase):
    password: str

    def __init__(self, password: str, **kwargs) -> None:
        password = self.get_password_hash(password)
        super().__init__(password=password, **kwargs)
