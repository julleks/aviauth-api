from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_versioning import version
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import create_access_token
from app.core.backends import oauth2_scheme
from app.core.config import settings
from app.core.permissions import PermissionsDependency, ReadUserPermission
from app.crud import users
from app.db.session import get_session
from app.models.access_tokens import AccessTokenRead
from app.models.users import UserCreate, UserRead

router = APIRouter()


@version(0)
@router.post("/register", response_model=AccessTokenRead)
async def register(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
) -> AccessTokenRead:
    user = await users.create(
        session, UserCreate(username=form_data.username, password=form_data.password)
    )
    user = await users.create(session, user)

    if not form_data.scopes:
        scope = " ".join(settings.OAUTH2_SCOPES.keys())
    else:
        scope = form_data.scopes

    return await create_access_token(
        session, form_data.client_id, form_data.client_secret, user.id, scope
    )


@version(0)
@router.get(
    "/profile",
    response_model=UserRead,
    dependencies=[Depends(PermissionsDependency([ReadUserPermission]))],
)
async def get_profile(
    request: Request,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    return request.user
