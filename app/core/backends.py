# Reference:
# https://fastapi-contrib.readthedocs.io/en/latest/_modules/fastapi_contrib/auth/backends.html

from typing import Optional, Tuple, Union

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from starlette.authentication import AuthenticationBackend, AuthenticationError
from starlette.requests import HTTPConnection

from app.core.config import settings
from app.db.session import get_session
from app.models.users import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token",
    scopes=settings.OAUTH2_SCOPES,
)


async def authenticate_user(
    session: AsyncSession, username: str, password: str
) -> Union[User, bool]:

    statement = select(User).where(User.username == username)
    results = await session.execute(statement)
    user = results.scalar()

    if not user:
        return False

    if not user.check_password(password):
        return False

    return user


class OAuthAuthenticationBackend(AuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection, session: AsyncSession = Depends(get_session)
    ) -> Optional[Tuple[bool, User]]:  # -> Optional[Tuple["AuthCredentials", User]]:
        authorization: str = conn.headers.get("Authorization")

        if not authorization:
            return False, None

        scheme, credentials = get_authorization_scheme_param(authorization)

        if not (authorization and scheme and credentials):
            raise AuthenticationError("Not authenticated")

        if scheme.lower() != "token":
            return False, None

        # token = await AccessToken.get(
        #     key=credentials,
        #     is_active=True,
        #     expires={"$not": {"$lt": get_now()}},
        # )

        # if token is None:
        #     return False, None

        # conn.scope["token"] = token

        # user = await User.get(id=token.user_id)
        #
        # if user is None:
        #     return False, None

        # return True, user

        return True, {}


oauth2_backend = OAuthAuthenticationBackend()
