from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings

__all__ = ["oauth2_scheme"]


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=settings.TOKEN_PATH,
    scopes=settings.OAUTH2_SCOPES,
)
