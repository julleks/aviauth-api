from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_versioning import version
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import create_access_token
from app.core.exceptions import InvalidCredentials
from app.crud import users
from app.db.session import get_session
from app.models.access_tokens import AccessTokenRead

router = APIRouter()


@version(0)
@router.post("/token", response_model=AccessTokenRead)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
) -> AccessTokenRead:

    user = await users.get_by_username(session, form_data.username)

    scope = " ".join(form_data.scopes)

    if not (user and user.verify_password(form_data.password)):
        raise InvalidCredentials(
            authenticate_value=f"Bearer scope = '{scope}'",
        )

    return await create_access_token(
        session, form_data.client_id, form_data.client_secret, user.id, scope
    )
