from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi_versioning import version
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.backends import oauth2_scheme
from app.core.permissions import (
    PermissionsDependency,
    WriteApplicationPermission,
)
from app.crud import applications
from app.db.session import get_session
from app.models.applications import (
    Application,
    ApplicationCreate,
    ApplicationRead,
)

router = APIRouter()


@version(0)
@router.post(
    "/register",
    response_model=ApplicationRead,
    dependencies=[Depends(PermissionsDependency([WriteApplicationPermission]))],
)
async def register(
    request: Request,
    application: ApplicationCreate,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> ApplicationRead:
    application = Application(user_id=request.user.id, **application.dict())
    application = await applications.create(session, application)
    return application
