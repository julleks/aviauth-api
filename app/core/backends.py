from typing import Optional, Tuple

from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from starlette.authentication import AuthCredentials
from starlette.requests import HTTPConnection

from app.core.config import settings
from app.crud import access_tokens, users
from app.db.session import async_session
from app.models.users import UserRead

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token",
    scopes=settings.OAUTH2_SCOPES,
)


class OAuthAuthenticationBackend:
    async def authenticate(
        self,
        conn: HTTPConnection,
    ) -> Optional[Tuple[AuthCredentials, UserRead]]:
        authorization: str = conn.headers.get("Authorization")
        import pprint

        pprint.pprint(conn.headers)
        if not authorization:
            return

        scheme, access_token = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and access_token):
            return

        if scheme.lower() != "bearer":
            return

        async with async_session() as session:
            access_token = await access_tokens.get_active(session, access_token)

        if not access_token:
            return

        # TODO: Add backwards relation to user from access token
        async with async_session() as session:
            user = await users.get(session, access_token.user_id)

        return AuthCredentials(scopes=access_token.scopes_list), UserRead(**user.dict())


oauth2_backend = OAuthAuthenticationBackend()
