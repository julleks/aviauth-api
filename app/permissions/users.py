from app.permissions.base import IsAuthenticated

__all__ = ["ReadUserPermission"]


class ReadUserPermission(IsAuthenticated):
    scopes = ["user:read", "user:full"]
