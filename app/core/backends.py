from typing import Optional, Tuple

from fastapi.security.utils import get_authorization_scheme_param
from starlette.authentication import AuthCredentials
from starlette.requests import HTTPConnection

from app.crud import access_tokens, users
from app.db.session import async_session
from app.models.users import UserRead

__all__ = ["oauth2_backend"]


class OAuthBackend:
    async def authenticate(
        self,
        conn: HTTPConnection,
    ) -> Optional[Tuple[AuthCredentials, UserRead]]:
        authorization: str = conn.headers.get("Authorization")

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


oauth2_backend = OAuthBackend()
