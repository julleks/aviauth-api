from fastapi import HTTPException
from starlette import status

__all__ = ["InactiveUser", "InvalidUserCredentials", "EmailAlreadyExists"]


class InactiveUser(HTTPException):
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
        **kwargs,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, **kwargs)


class EmailAlreadyExists(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "User with this email already registered.",
        **kwargs,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, **kwargs)
