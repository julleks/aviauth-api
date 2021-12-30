from fastapi import APIRouter, Depends, status
from fastapi.requests import Request
from fastapi_versioning import version
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import OAuth2EmailPasswordRequestForm, oauth2_scheme
from app.core.config import settings
from app.core.dependencies import PermissionsDependency
from app.crud import access_tokens, users
from app.db.session import get_session
from app.exceptions import EmailAlreadyExists
from app.models.access_tokens import AccessTokenRead
from app.models.users import UserCreate, UserRead
from app.permissions import NotAuthenticated, ReadUserPermission

router = APIRouter()


@version(0)
@router.post(
    "/register",
    response_model=AccessTokenRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(PermissionsDependency([NotAuthenticated]))],
)
async def register(
    form_data: OAuth2EmailPasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
) -> AccessTokenRead:

    try:
        user = await users.create(
            session, UserCreate(email=form_data.email, password=form_data.password)
        )
    except IntegrityError:
        raise EmailAlreadyExists

    if not form_data.scopes:
        scope = " ".join(settings.OAUTH2_SCOPES.keys())
    else:
        scope = form_data.scopes

    return await access_tokens.create_access_token(
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
) -> UserRead:
    return request.user
