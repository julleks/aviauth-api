from typing import Dict, Optional

from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: str = "Could not validate credentials",
        headers: Optional[Dict[str, str]] = None,
        authenticate_value: str = "Bearer",
    ) -> None:

        if not headers:
            headers = ({"WWW-Authenticate": authenticate_value},)

        super().__init__(status_code=status_code, detail=detail, headers=headers)


class NotEnoughPermissionsException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: str = "Not enough permissions",
        headers: Optional[Dict[str, str]] = None,
        authenticate_value: str = "Bearer",
    ) -> None:
        if not headers:
            headers = ({"WWW-Authenticate": authenticate_value},)

        super().__init__(status_code=status_code, detail=detail, headers=headers)


class InactiveUserException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "User is inactive",
        **kwargs,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, **kwargs)
