# Reference:
# https://fastapi-contrib.readthedocs.io/en/latest/_modules/fastapi_contrib/auth/backends.html

from datetime import datetime
from typing import Optional, Tuple, Union

from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from starlette.authentication import AuthCredentials, AuthenticationBackend
from starlette.requests import HTTPConnection

from app.core.config import settings
from app.db.session import async_session
from app.models.access_token import AccessToken
from app.models.users import User, UserRead

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
        self,
        conn: HTTPConnection,
    ) -> Optional[Tuple[AuthCredentials, UserRead]]:
        authorization: str = conn.headers.get("Authorization")
        # TODO: get client id and client secret from request

        if not authorization:
            return

        scheme, access_token = get_authorization_scheme_param(authorization)

        if not (authorization and scheme and access_token):
            return

        if scheme.lower() != "bearer":
            return

        async with async_session() as session:
            # TODO: include client id and client secret check
            statement = select(AccessToken).where(
                AccessToken.access_token == access_token,
                AccessToken.expires_at > datetime.now(),
                AccessToken.is_active,
            )
            results = await session.execute(statement)
            access_token = results.scalar()

        if not access_token:
            return

        async with async_session() as session:
            # TODO: include client id and client secret check
            statement = select(User).where(
                User.id == access_token.user_id,
            )
            results = await session.execute(statement)
            user = results.scalar()

        return AuthCredentials(scopes=access_token.scope), UserRead(**user.dict())


oauth2_backend = OAuthAuthenticationBackend()
