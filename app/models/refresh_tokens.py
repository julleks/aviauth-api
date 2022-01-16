from typing import Optional
from uuid import UUID, uuid4

from jose import jwt
from sqlmodel import Column, DateTime, Field, Relationship

from app.core.config import settings
from app.core.datetime import datetime, timedelta
from app.packages.sqlmodel import SQLModel


class RefreshToken(SQLModel, table=True):
    """
    Refresh token is a credential artifact that lets a client application
    get new access tokens without having to ask the user to log in again.
    """

    id: UUID = Field(
        primary_key=True,
        default_factory=uuid4,
        nullable=False,
        sa_column_kwargs=dict(unique=True),
    )
    token: str = Field(nullable=False, sa_column_kwargs=dict(unique=True))
    # TODO: Pass ondelete="CASCADE" to ForeignKey object when available
    user_id: UUID = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="refresh_tokens")

    # TODO: Pass ondelete="CASCADE" to ForeignKey object when available
    client_id: Optional[str] = Field(foreign_key="application.client_id", nullable=True)
    application: "Application" = Relationship(back_populates="refresh_tokens")

    # related_access_token_id: str = Field(
    #     foreign_key="accesstoken.id",
    #     nullable=True,
    # )

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)), default_factory=datetime.now
    )
    revoked_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True)), nullable=True
    )

    def __init__(self, scope: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.token = self.get_token_hash(scope)

    def get_token_hash(self, scope: str) -> str:
        payload = {
            "exp": self.created_at + timedelta(seconds=settings.REFRESH_TOKEN_LIFETIME),
            "iat": self.created_at,
            "scope": scope,
            "sub": str(self.user_id),
            "aud": settings.TOKEN_URL,
            "iss": settings.API_URL,
            "azp": self.client_id,
        }

        return jwt.encode(
            payload, settings.SECRET_KEY, algorithm=settings.TOKEN_HASH_ALGORITHM
        )
