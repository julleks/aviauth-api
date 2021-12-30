from fastapi import APIRouter, Depends, status
from fastapi.requests import Request
from fastapi_versioning import version
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import oauth2_scheme
from app.core.dependencies import PermissionsDependency
from app.crud import applications
from app.db.session import get_session
from app.exceptions import ApplicationAlreadyExists
from app.models.applications import (
    Application,
    ApplicationCreate,
    ApplicationRead,
)
from app.permissions import CreateApplicationsPermission

router = APIRouter()


@version(0)
@router.post(
    "/register",
    response_model=ApplicationRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(PermissionsDependency([CreateApplicationsPermission]))],
)
async def register(
    request: Request,
    application: ApplicationCreate,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> ApplicationRead:
    application = Application(user_id=request.user.id, **application.dict())
    try:
        application = await applications.create(session, application)
    except IntegrityError:
        raise ApplicationAlreadyExists

    return application
