from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_versioning import version
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import PermissionsDependency
from app.crud import access_tokens, users
from app.db.session import get_session
from app.exceptions import InvalidUserCredentials
from app.models.access_tokens import AccessTokenRead
from app.permissions import NotAuthenticated

router = APIRouter()


@version(0)
@router.post(
    "/token",
    response_model=AccessTokenRead,
    dependencies=[Depends(PermissionsDependency([NotAuthenticated]))],
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
) -> AccessTokenRead:

    user = await users.get_by_email(session, form_data.username)

    if not (user and user.check_password(form_data.password)):
        raise InvalidUserCredentials()

    scope = " ".join(form_data.scopes)

    return await access_tokens.create_access_token(
        session, form_data.client_id, form_data.client_secret, user.id, scope
    )


# TODO: add authorize endpoint
