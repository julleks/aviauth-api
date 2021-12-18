from datetime import datetime, timedelta
from uuid import UUID, uuid4

from jose import jwt
from sqlmodel import Field, SQLModel

from app.core.config import settings


class AccessTokenBase(SQLModel):
    access_token: str  # TODO: set unique = True and check max length to be 255
    token_type: str  # Choices: Bearer


class AccessToken(AccessTokenBase, table=True):
    id: UUID = Field(primary_key=True)

    user_id: UUID = Field(foreign_key="user.id")

    # source_refresh_token: UUID = Field(
    #     foreign_key="refresh_token.id", nullable=True
    # )  # TODO: set unique source_refresh_token + id

    scope: str  # TODO: use sqlmodel Text field
    expires_at: datetime  # TODO: use sqlmodel datetime with timezone field

    # id_token: UUID = Field(
    #     foreign_key="id_token.id", nullable=True
    # )  # TODO: set unique id_token + id

    # application: UUID = Field(foreign_key="application.id", nullable=True)

    created_at: datetime  # TODO: use sqlmodel datetime with timezone field

    is_active: bool = True

    def __init__(self, user_id, scope, **kwargs):
        self.id = uuid4()
        self.created_at = datetime.now()  # TODO: pass a timezone
        self.expires_at = self.created_at + timedelta(
            seconds=settings.ACCESS_TOKEN_LIFETIME
        )

        to_encode = {
            "sub": str(user_id),
            "scopes": scope.replace(", ", "").split(","),
            "exp": self.expires_at,
        }

        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.HASH_ALGORITHM
        )

        self.access_token = encoded_jwt
        self.token_type = "bearer"

        super().__init__(user_id=user_id, scope=scope, **kwargs)

    # def get_data(self):
    #     try:
    #         payload = jwt.decode(
    #             self.token,
    #             settings.SECRET_KEY,
    #             algorithms=[settings.HASH_ALGORITHM],
    #         )
    #         username: str = payload.get("sub")
    #
    #         if username is None:
    #             return None
    #
    #         token_data = TokenData(username=username)
    #
    #     except JWTError:
    #         return None
    #
    #     return token_data


class AccessTokenRead(AccessTokenBase):
    # TODO: get expires_in from a Class instead of providing it from the API
    # Access Token response specification:
    # https://www.tutorialspoint.com/oauth2.0/access_token_response.htm
    expires_in: int = settings.ACCESS_TOKEN_LIFETIME

    refresh_token: str = None
