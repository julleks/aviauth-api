from app.permissions.base import IsAuthenticated

__all__ = ["ReadUserPermission"]


class ReadUserPermission(IsAuthenticated):
    scope = "user:read"
