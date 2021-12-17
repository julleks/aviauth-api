# TODO: move to core

from typing import Union

from fastapi import Depends, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.config import settings
from app.core.exceptions import (
    CredentialsException,
    InactiveUserException,
    NotEnoughPermissionsException,
)
from app.db.session import get_session
from app.models.auth import TokenData
from app.models.users import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token",
    scopes=settings.OAUTH2_SCOPES,
)


async def authenticate_user(
    session: AsyncSession, username: str, password: str
) -> Union[User, bool]:

    statement = select(User).where(User.username == username)
    results = await session.execute(statement)
    user = results.scalar()

    if not user:
        return False

    if not user.check_password(password):
        return False

    return user


async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> User:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.HASH_ALGORITHM]
        )

        username: str = payload.get("sub")

        if username is None:
            raise CredentialsException(authenticate_value=authenticate_value)

        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)

    except JWTError:
        raise CredentialsException(authenticate_value=authenticate_value)

    statement = select(User).where(User.username == token_data.username)
    results = await session.execute(statement)
    user = results.scalar()

    if user is None:
        raise CredentialsException(authenticate_value=authenticate_value)

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise NotEnoughPermissionsException(authenticate_value=authenticate_value)

    return user


async def get_current_active_user(
    current_user: User = Security(get_current_user, scopes=["user:read"])
) -> User:
    if not current_user.is_active:
        raise InactiveUserException()
    return current_user
