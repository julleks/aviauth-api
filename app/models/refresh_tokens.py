from typing import Optional
from uuid import UUID

from jose import jwt
from sqlmodel import Column, DateTime, Field, Relationship

from app.core.config import settings
from app.core.datetime import datetime, timedelta
from app.packages.sqlmodel import SQLModel


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
    user: "User" = Relationship(back_populates="refresh_tokens")

    # TODO: Pass ondelete="CASCADE" to ForeignKey object when available
    application_id: Optional[str] = Field(
        foreign_key="application.client_id", nullable=True
    )

    access_token: str = Field(
        foreign_key="accesstoken.access_token",
        nullable=True,
    )

    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True)), nullable=True
    )
    revoked_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True)), nullable=True
    )

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
            payload, settings.SECRET_KEY, algorithm=settings.TOKEN_HASH_ALGORITHM
        )

        super().__init__(**kwargs)
