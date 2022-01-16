from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.requests import Request
from fastapi_versioning import version
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import OAuth2EmailPasswordRequestForm, oauth2_scheme
from app.core.config import settings
from app.core.dependencies import PermissionsDependency
from app.core.tokens import email_confirmation_token_generator
from app.crud import access_tokens, users
from app.db.session import get_session
from app.exceptions import EmailAlreadyExists
from app.models.access_tokens import AccessTokenRead
from app.models.users import UserCreate, UserRead
from app.permissions import NotAuthenticated, ReadUserPermission
from app.services import email_client

router = APIRouter()


@version(0)
@router.post(
    "/register",
    response_model=AccessTokenRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(PermissionsDependency([NotAuthenticated]))],
)
async def register(
    background_tasks: BackgroundTasks,
    form_data: OAuth2EmailPasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
) -> AccessTokenRead:

    await session.begin_nested()
    try:
        try:
            user = await users.create(
                session, UserCreate(email=form_data.email, password=form_data.password)
            )
        except IntegrityError:
            raise EmailAlreadyExists

        if not form_data.scopes:
            scopes = settings.OAUTH2_SCOPES.keys()
        else:
            scopes = form_data.scopes

        scope = " ".join(scopes)

        access_token = await access_tokens.create_access_token(
            session, form_data.client_id, form_data.client_secret, user.id, scope
        )

        background_tasks.add_task(email_client.send_registration_email, user)

    except Exception as e:
        raise e

    return access_token


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


@version(0)
@router.get(
    "/verify",
)
async def verify_email(
    id: str,
    token: str,
    session: AsyncSession = Depends(get_session),
):
    user = await users.get(session, id)

    if email_confirmation_token_generator.check_token(user, token):
        await users.verify_email(session, user)

        return {"message": "Email verified"}

    return {"message": "Invalid token or email have been already verified."}
