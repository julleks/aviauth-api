from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field

from app.core.security import get_password_hash, verify_password
from app.packages.sqlmodel import SQLModel


class UserBase(SQLModel):
    username: str = Field(max_length=64, sa_column_kwargs={"unique": True})
    email: Optional[str] = Field(max_length=64, sa_column_kwargs={"unique": True})
    first_name: Optional[str] = Field(max_length=64, default="", nullable=False)
    last_name: Optional[str] = Field(max_length=64, default="", nullable=False)

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.username

    @staticmethod
    def get_password_hash(password):
        return get_password_hash(password)


class UserRead(UserBase):
    id: UUID


class UnauthenticatedUser(UserRead):
    pass

    @property
    def is_authenticated(self) -> bool:
        return False

    @property
    def display_name(self) -> str:
        return "Anonymous"


class User(UserRead, table=True):
    id: UUID = Field(
        primary_key=True,
        default_factory=uuid4,
        nullable=False,
        sa_column_kwargs=dict(unique=True),
    )
    password: str = Field(max_length=255, index=False, nullable=True)
    is_active: bool = Field(default=True, nullable=False)

    def verify_password(self, password: str) -> bool:
        return verify_password(password, self.password)


class UserCreate(UserBase):
    password: str

    def __init__(self, password: str, **kwargs) -> None:
        password = self.get_password_hash(password)
        super().__init__(password=password, **kwargs)
