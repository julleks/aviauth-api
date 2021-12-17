from fastapi import APIRouter, Depends
from fastapi_versioning import version
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.auth import AccessToken
from app.models.users import User, UserCreate, UserRead
from app.services.auth import get_current_active_user

router = APIRouter()


@version(0)
@router.post("/register", response_model=AccessToken)
async def register(
    user: UserCreate, session: AsyncSession = Depends(get_session)
) -> AccessToken:
    user = User(**user.dict())
    session.add(user)
    await session.commit()

    return AccessToken.create(user, scopes=["user:read"])


@version(0)
@router.get("/profile", response_model=UserRead)
async def get_profile(current_user: User = Depends(get_current_active_user)):
    return current_user
