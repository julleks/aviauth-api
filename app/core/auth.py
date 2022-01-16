from typing import Optional

from fastapi.param_functions import Form
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr

from app.core.config import settings

__all__ = ["oauth2_scheme", "OAuth2EmailPasswordRequestForm"]


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=settings.TOKEN_PATH,
    scopes=settings.OAUTH2_SCOPES,
)


class OAuth2EmailPasswordRequestForm:
    def __init__(
        self,
        grant_type: str = Form("password", regex="password"),
        email: EmailStr = Form(...),
        password: str = Form(...),
        scope: str = Form(""),
        client_id: Optional[str] = Form(None),
        client_secret: Optional[str] = Form(None),
    ):
        self.grant_type = grant_type
        self.email = email
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret
