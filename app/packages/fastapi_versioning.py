# Custom FastAPI versioning with major version in path
# Based on https://github.com/DeanWay/fastapi-versioning
# ToDo: separate to a package


from collections import defaultdict
from typing import Any, Callable, Dict, List, Tuple, Type, TypeVar, cast

from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.routing import BaseRoute

CallableT = TypeVar("CallableT", bound=Callable[..., Any])


def version(
    major: int, minor: int = 0, patch: int = 0
) -> Callable[[CallableT], CallableT]:
    def decorator(func: CallableT) -> CallableT:
        func._api_version = (major, minor, patch)  # type: ignore
        return func

    return decorator


def version_to_route(
    route: BaseRoute,
    default_version: Tuple[int, int, int],
) -> Tuple[Tuple[int, int, int], APIRoute]:
    api_route = cast(APIRoute, route)
    version = getattr(api_route.endpoint, "_api_version", default_version)
    return version, api_route


def VersionedFastAPI(
    app: FastAPI,
    version_format: str = "{major}.{minor}.{patch}",
    prefix_format: str = "/v{major}",
    default_version: Tuple[int, int, int] = (0, 1, 0),
    enable_latest: bool = True,
    **kwargs: Any,
) -> FastAPI:
    parent_app = FastAPI(
        title=app.title,
        **kwargs,
    )
    version_route_mapping: Dict[int, List[APIRoute]] = defaultdict(list)
    version_routes = [version_to_route(route, default_version) for route in app.routes]

    # list of all versions found in the routes
    versions = [route[0] for route in version_routes]

    versions = sorted(versions, reverse=True)

    versions_mapping = {}

    for route_version in versions:
        # map major with the latest minor and patch versions

        major_version = route_version[0]

        if not versions_mapping.get(major_version):
            versions_mapping[major_version] = route_version

    for route_version, route in version_routes:
        # map routes according to major versions
        version_route_mapping[versions_mapping.get(route_version[0])].append(route)

    unique_routes = {}

    for version in sorted(versions_mapping.values()):
        major, minor, patch = version

        prefix = prefix_format.format(major=major)
        semver = version_format.format(major=major, minor=minor, patch=patch)

        versioned_app = FastAPI(
            title=app.title,
            description=app.description,
            version=semver,
        )

        for route in version_route_mapping[version]:
            for method in route.methods:
                unique_routes[route.path + "|" + method] = route

        for route in unique_routes.values():
            versioned_app.router.routes.append(route)

        parent_app.mount(prefix, versioned_app)

        @parent_app.get(f"{prefix}/openapi.json", name=semver, tags=["Versions"])
        @parent_app.get(f"{prefix}/docs", name=semver, tags=["Documentations"])
        def noop() -> None:
            ...

    if enable_latest:
        prefix = "/latest"

        major, minor, patch = version

        semver = version_format.format(major=major, minor=minor, patch=patch)

        versioned_app = FastAPI(
            title=app.title,
            description=app.description,
            version=semver,
        )

        for route in unique_routes.values():
            versioned_app.router.routes.append(route)

        parent_app.mount(prefix, versioned_app)

    return parent_app


def versioned_api_route(
    major: int = 1,
    minor: int = 0,
    patch: int = 0,
    route_class: Type[APIRoute] = APIRoute,
) -> Type[APIRoute]:
    class VersionedAPIRoute(route_class):  # type: ignore
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
            try:
                self.endpoint._api_version = (major, minor, patch)
            except AttributeError:
                # Support bound methods
                self.endpoint.__func__._api_version = (major, minor)

    return VersionedAPIRoute
