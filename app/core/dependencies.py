from starlette.requests import Request

__all__ = ["PermissionsDependency"]


class PermissionsDependency:
    def __init__(self, permissions_classes: list):
        self.permissions_classes = permissions_classes

    def __call__(self, request: Request):
        for permission_class in self.permissions_classes:
            permission_class(request=request)
