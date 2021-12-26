from uuid import UUID

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import InvalidClientCredentials
from app.crud import access_tokens, applications, refresh_tokens
from app.models.access_tokens import AccessToken, AccessTokenRead
from app.models.refresh_tokens import RefreshToken

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=settings.TOKEN_PATH,
    scopes=settings.OAUTH2_SCOPES,
)


async def create_access_token(
    session: AsyncSession, client_id: str, client_secret: str, user_id: UUID, scope: str
) -> AccessTokenRead:
    application = await applications.get(session, client_id)

    if not (application and application.verify_secret(client_secret)):
        await session.rollback()
        raise InvalidClientCredentials

    refresh_token = await refresh_tokens.create(
        session,
        RefreshToken(
            user_id=user_id, scope=scope, application_id=application.client_id
        ),
    )
    access_token = await access_tokens.create(
        session,
        AccessToken(
            user_id=user_id,
            scope=scope,
            refresh_token=refresh_token.token,
            application_id=application.client_id,
        ),
    )

    return AccessTokenRead(**access_token.dict())
