from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel

from app.services.security import get_password_hash, verify_password


class UserBase(SQLModel):
    username: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserRead(UserBase):
    id: UUID = Field(primary_key=True)


class User(UserRead, table=True):
    password: str = None
    is_active: bool = True

    def __init__(self, password: str, **kwargs) -> None:
        user_id = uuid4()
        password = get_password_hash(password)
        super().__init__(id=user_id, password=password, **kwargs)

    def check_password(self, password: str) -> bool:
        return verify_password(password, self.password)


class UserCreate(UserBase):
    password: str
