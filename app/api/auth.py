from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_versioning import version
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.access_tokens import access_tokens
from app.crud.users import users
from app.db.session import get_session
from app.exceptions.users import InvalidUserCredentials
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
        raise InvalidUserCredentials(
            authenticate_value=f"Bearer scope = '{scope}'",
        )

    return await access_tokens.create_access_token(
        session, form_data.client_id, form_data.client_secret, user.id, scope
    )
