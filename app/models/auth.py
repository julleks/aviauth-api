from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID, uuid4

from jose import JWTError, jwt
from sqlmodel import Field, SQLModel

from app.core.config import settings
from app.models.users import User


class Application(SQLModel):
    pass


class Grant(SQLModel):
    pass


class AccessToken(SQLModel):
    id: UUID
    user: UUID = Field(foreign_key="user.id")
    source_refresh_token: UUID = Field(
        foreign_key="refresh_token.id", nullable=True
    )  # TODO: set unique source_refresh_token + id
    token: str  # TODO: set unique = True and check max length to be 255
    token_type: str  # Choices: Bearer
    id_token: UUID = Field(
        foreign_key="id_token.id", nullable=True
    )  # TODO: set unique id_token + id
    application: UUID = Field(foreign_key="application.id", nullable=True)
    expires_at: datetime  # TODO: use sqlmodel datetime with timezone field
    scope: str  # TODO: use sqlmodel Text field
    created_at: datetime  # TODO: use sqlmodel datetime with timezone field

    def __init__(self, **kwargs):
        self.id = uuid4()
        self.created_at = datetime.now()  # TODO: pass a timezone
        super().__init__(**kwargs)

    @classmethod
    def create(
        cls,
        user: User,
        scopes: Optional[List[str]] = None,
        expires_delta: Optional[timedelta] = timedelta(
            seconds=settings.ACCESS_TOKEN_LIFETIME
        ),
    ):
        expire = datetime.utcnow() + expires_delta

        to_encode = {
            "sub": user.username,
            "scopes": scopes,
            "exp": expire,
        }

        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.HASH_ALGORITHM
        )

        return cls(
            token=encoded_jwt,
            token_type="bearer",
            expires_in=expires_delta.seconds,
        )

    def get_data(self):
        try:
            payload = jwt.decode(
                self.token,
                settings.SECRET_KEY,
                algorithms=[settings.HASH_ALGORITHM],
            )
            username: str = payload.get("sub")

            if username is None:
                return None

            token_data = TokenData(username=username)

        except JWTError:
            return None

        return token_data


class TokenData(SQLModel):
    username: Optional[str] = None
    scopes: List[str] = []


class RefreshToken(SQLModel):
    pass


class IDToken(SQLModel):
    pass
