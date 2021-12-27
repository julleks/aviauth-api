from typing import Dict, Optional

from fastapi import HTTPException
from starlette import status

__all__ = ["InactiveUserException"]


class InactiveUserException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "Inactive user",
        **kwargs,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, **kwargs)


class InvalidUserCredentials(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: str = "Invalid user credentials",
        headers: Optional[Dict[str, str]] = None,
        authenticate_value: str = "Bearer",
    ) -> None:

        if not headers:
            headers = ({"WWW-Authenticate": authenticate_value},)

        super().__init__(status_code=status_code, detail=detail, headers=headers)
