from starlette import status
from starlette.requests import Request

from app.exceptions.base import NotEnoughPermissions

__all__ = ["IsAuthenticated"]


class BasePermission:
    error_message = "Forbidden"
    status_code = status.HTTP_403_FORBIDDEN

    def has_required_permissions(self, request: Request) -> bool:
        raise NotImplementedError()

    def __init__(self, request: Request):
        if not self.has_required_permissions(request):
            raise NotEnoughPermissions(
                status_code=self.status_code,
                detail=self.error_message,
            )


class IsAuthenticated(BasePermission):
    error_message = "Not authenticated"
    scope = ""

    def has_required_permissions(self, request: Request) -> bool:
        if not request.user.is_authenticated:
            self.status_code = status.HTTP_401_UNAUTHORIZED
            return False

        if self.scope not in request.auth.scopes:
            return False

        return True
