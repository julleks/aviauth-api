from typing import Dict, Optional

from fastapi import HTTPException
from starlette import status

__all__ = ["NotEnoughPermissions"]


class NotEnoughPermissions(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: str = "Unauthorized",
        headers: Optional[Dict[str, str]] = None,
        authenticate_value: str = "Bearer",
    ) -> None:
        if not headers:
            headers = {"WWW-Authenticate": authenticate_value}

        super().__init__(status_code=status_code, detail=detail, headers=headers)
