from app.permissions.base import IsAuthenticated

__all__ = ["WriteApplicationsPermission"]


class WriteApplicationsPermission(IsAuthenticated):
    scope = "applications:write"
