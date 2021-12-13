from datetime import datetime, timedelta
from typing import List, Optional

from jose import JWTError, jwt
from sqlmodel import SQLModel

from app.core.config import settings
from app.models.users import User


class Token(SQLModel):
    access_token: str
    token_type: str
    expires_in: timedelta

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
            access_token=encoded_jwt,
            token_type="bearer",
            expires_in=expires_delta.seconds,
        )

    def get_data(self):
        try:
            payload = jwt.decode(
                self.access_token,
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
