from fastapi import HTTPException
from starlette import status

__all__ = ["InvalidClientCredentials"]


class InvalidClientCredentials(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "Invalid client credentials",
        **kwargs,
    ):
        super().__init__(status_code=status_code, detail=detail, **kwargs)
