from fastapi.exceptions import HTTPException
from starlette import status
from starlette.requests import Request


class BasePermission:
    error_message = "Forbidden"
    status_code = status.HTTP_403_FORBIDDEN

    def has_required_permissions(self, request: Request) -> bool:
        raise NotImplementedError()

    def __init__(self, request: Request):
        if not self.has_required_permissions(request):
            raise HTTPException(
                status_code=self.status_code,
                detail=self.error_message,
            )


class IsAuthenticated(BasePermission):
    error_msg = "Not authenticated"
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = status.HTTP_401_UNAUTHORIZED

    def has_required_permissions(self, request: Request) -> bool:
        return request.user.is_authenticated


class ReadUserPermission(BasePermission):
    error_msg = "Not authenticated"
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = status.HTTP_401_UNAUTHORIZED

    def has_required_permissions(self, request: Request) -> bool:
        return (
            super().has_required_permissions(request)
            and "user:read" in request.auth.scopes
        )


class WriteApplicationPermission(IsAuthenticated):
    error_msg = "Not authenticated"
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = status.HTTP_401_UNAUTHORIZED

    def has_required_permissions(self, request: Request) -> bool:
        return (
            super().has_required_permissions(request)
            and "applications:write" in request.auth.scopes
        )


class PermissionsDependency:
    def __init__(self, permissions_classes: list):
        self.permissions_classes = permissions_classes

    def __call__(self, request: Request):
        for permission_class in self.permissions_classes:
            permission_class(request=request)
