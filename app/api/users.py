from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi_versioning import version
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.access_token import AccessToken, AccessTokenRead
from app.models.users import User, UserCreate, UserRead

router = APIRouter()


@version(0)
@router.post("/register", response_model=AccessTokenRead)
async def register(
    user: UserCreate, session: AsyncSession = Depends(get_session)
) -> AccessTokenRead:

    user = User(**user.dict())
    session.add(user)

    await session.commit()

    access_token = AccessToken(user_id=user.id, scope="user:read")
    session.add(access_token)

    await session.commit()

    return AccessTokenRead(**access_token.dict())


@version(0)
@router.get("/profile", response_model=UserRead)
async def get_profile(request: Request):
    return request.user
