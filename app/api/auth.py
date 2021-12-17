# Reference:
# https://github.com/jazzband/django-oauth-toolkit/blob/master/oauth2_provider/models.py

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_versioning import version
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import CredentialsException
from app.db.session import get_session
from app.models.auth import AccessToken
from app.services.auth import authenticate_user

router = APIRouter()


@version(0)
@router.post("/token", response_model=AccessToken)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(session, form_data.username, form_data.password)

    if not user:
        raise CredentialsException(
            authenticate_value=f"Bearer scopes = '{','.join(form_data.scopes)}",
        )

    access_token = AccessToken.create(user, form_data.scopes)

    return access_token
