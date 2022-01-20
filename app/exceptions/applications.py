from fastapi import HTTPException
from starlette import status

__all__ = ["InvalidClientCredentials", "ApplicationAlreadyExists"]


class InvalidClientCredentials(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: str = "Invalid client credentials",
        **kwargs,
    ):
        super().__init__(status_code=status_code, detail=detail, **kwargs)


class ApplicationAlreadyExists(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "Application with this client_id already registered",
        **kwargs,
    ):
        super().__init__(status_code=status_code, detail=detail, **kwargs)
