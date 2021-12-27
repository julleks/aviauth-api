from typing import Optional
from uuid import UUID

from jose import jwt
from sqlmodel import Field, SQLModel

from app.core.config import settings
from app.core.datetime import datetime, timedelta


class RefreshToken(SQLModel, table=True):
    """
    More about Refresh Tokens:
    https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/
    """

    token: str = Field(
        primary_key=True, nullable=False, sa_column_kwargs=dict(unique=True)
    )
    # TODO: Pass ondelete="CASCADE" to ForeignKey object when available
    user_id: UUID = Field(foreign_key="user.id")

    # TODO: Pass ondelete="CASCADE" to ForeignKey object when available
    application_id: Optional[str] = Field(
        foreign_key="application.client_id", nullable=True
    )

    access_token: str = Field(
        foreign_key="accesstoken.access_token",
        # sa_column_kwargs=dict(unique=True),
        nullable=True,
    )

    created_at: datetime = Field(nullable=True)
    updated_at: Optional[datetime] = Field(nullable=True)
    revoked_at: Optional[datetime] = Field(nullable=True)

    def __init__(self, user_id, scope, **kwargs):
        self.created_at = datetime.now()

        self.user_id = user_id

        payload = {
            "exp": self.created_at + timedelta(seconds=settings.REFRESH_TOKEN_LIFETIME),
            "iat": self.created_at,
            "scope": scope,
            "sub": str(self.user_id),
            "aud": settings.TOKEN_URL,
            "iss": settings.API_URL,
            "azp": self.application_id,
        }

        self.token = jwt.encode(
            payload, settings.SECRET_KEY, algorithm=settings.HASH_ALGORITHM
        )

        super().__init__(**kwargs)
