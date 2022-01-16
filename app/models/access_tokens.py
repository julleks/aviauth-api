from typing import Optional
from uuid import UUID, uuid4

from jose import jwt
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

from app.core.config import settings
from app.core.datetime import datetime, timedelta

__all__ = [
    "AccessTokenBase",
    "AccessTokenRead",
    "AccessToken",
]


class AccessTokenBase(SQLModel):
    """
    Access token is an artifact that client applications can use
    to make secure calls to an API server. When a client application
    needs to access protected resources on a server on behalf of a user,
    the access token lets the client signal to the server that it has received
    authorization by the user to perform certain tasks or access certain resources.
    """

    access_token: str = Field(
        primary_key=True, nullable=False, sa_column_kwargs=dict(unique=True)
    )
    token_type: str = Field(default="bearer", nullable=False)

    source_refresh_token: Optional[str] = Field(
        foreign_key="refreshtoken.token", nullable=True
    )


class AccessTokenRead(AccessTokenBase):
    # Access Token response specification:
    # https://www.tutorialspoint.com/oauth2.0/access_token_response.htm

    expires_in: int = settings.ACCESS_TOKEN_LIFETIME


class AccessToken(AccessTokenBase, table=True):
    # TODO: Pass ondelete="CASCADE" to ForeignKey object when available
    id: UUID = Field(
        primary_key=True,
        default_factory=uuid4,
        nullable=False,
        sa_column_kwargs=dict(unique=True),
    )
    user_id: UUID = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="access_tokens")

    scope: str = Field(index=False)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)), default_factory=datetime.now
    )
    expires_at: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    revoked_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True)), nullable=True
    )
    # id_token: str = Field(
    #     foreign_key="id_token.token", nullable=True, sa_column_kwargs={"unique": True}
    # )

    client_id: str = Field(foreign_key="application.client_id", nullable=True)
    application: "Application" = Relationship(back_populates="access_tokens")

    @property
    def is_active(self) -> bool:
        return bool((not self.revoked_at) and (self.expires_at > datetime.now()))

    @property
    def scopes_list(self) -> list:
        return self.scope.split(" ")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.expires_at = self.created_at + timedelta(
            seconds=settings.ACCESS_TOKEN_LIFETIME
        )
        self.access_token = self.get_token_hash()

    def get_token_hash(self) -> str:
        payload = {
            "iss": settings.API_URL,
            # TODO: update sub according to
            #  https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/
            "sub": str(self.user_id),
            # TODO: update aud according to
            #  https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/
            "aud": [],
            "azp": self.client_id,
            "exp": self.expires_at,
            "iat": self.created_at,
            "scope": self.scope,
            # TODO: update auth_time according to
            #  https://datatracker.ietf.org/doc/html/draft-bertocci-oauth-access-token-jwt-00#section-2.2.2
            # "auth_time": self.refresh_token.created_at,
        }

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.TOKEN_HASH_ALGORITHM,
        )
