from app.permissions.base import IsAuthenticated

__all__ = ["CreateApplicationsPermission"]


class CreateApplicationsPermission(IsAuthenticated):
    scopes = ["applications:create", "applications:full"]
