from typing import Optional
from uuid import UUID

from jose import jwt
from sqlmodel import Field, SQLModel

from app.core.config import settings
from app.core.datetime import datetime, timedelta

__all__ = [
    "AccessTokenBase",
    "AccessTokenRead",
    "AccessToken",
]


class AccessTokenBase(SQLModel):
    access_token: str = Field(
        primary_key=True, nullable=False, sa_column_kwargs=dict(unique=True)
    )
    token_type: str = Field(default="bearer", nullable=False)

    refresh_token: Optional[str] = Field(
        foreign_key="refreshtoken.token", nullable=True
    )


class AccessToken(AccessTokenBase, table=True):
    # TODO: Pass ondelete="CASCADE" to ForeignKey object when available
    user_id: UUID = Field(foreign_key="user.id")

    scope: str = Field(index=False)
    expires_at: datetime
    created_at: datetime

    # id_token: str = Field(
    #     foreign_key="id_token.token", nullable=True, sa_column_kwargs={"unique": True}
    # )

    application_id: Optional[str] = Field(
        foreign_key="application.client_id", nullable=True
    )

    is_active: bool = Field(default=True, nullable=False)

    @property
    def scopes_list(self):
        return self.scope.split(" ")

    def __init__(self, user_id, scope, **kwargs):
        self.created_at = datetime.now()

        self.user_id = user_id
        self.scope = scope

        self.expires_at = self.created_at + timedelta(
            seconds=settings.ACCESS_TOKEN_LIFETIME
        )

        payload = {
            "sub": str(user_id),
            "scopes": self.scopes_list,
            "exp": self.expires_at,
        }

        self.access_token = jwt.encode(
            payload, settings.SECRET_KEY, algorithm=settings.HASH_ALGORITHM
        )

        super().__init__(**kwargs)


class AccessTokenRead(AccessTokenBase):
    # Access Token response specification:
    # https://www.tutorialspoint.com/oauth2.0/access_token_response.htm

    expires_in: int = settings.ACCESS_TOKEN_LIFETIME
