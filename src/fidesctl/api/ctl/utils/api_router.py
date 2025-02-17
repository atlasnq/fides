"""Copy pasta'd from
https://github.com/ethyca/fidesops/blob/a072f2a987e0f02e96c3b63a500b7bd6d9c4c8db/src/fidesops/util/api_router.py
"""

from typing import Any, Callable

from fastapi import APIRouter as FastAPIRouter
from fastapi.types import DecoratedCallable


class APIRouter(FastAPIRouter):
    """
    Taken from: https://github.com/tiangolo/fastapi/issues/2060#issuecomment-834868906
    """

    def api_route(  # type: ignore
        self, path: str, *, include_in_schema: bool = True, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """
        Updated api_route function that automatically configures routes to have 2 versions.
        One without and trailing slash and another with it.
        """
        if path.endswith("/"):
            path = path[:-1]

        add_path = super().api_route(
            path, include_in_schema=include_in_schema, **kwargs
        )

        alternate_path = path + "/"
        add_alternate_path = super().api_route(
            alternate_path, include_in_schema=False, **kwargs
        )

        def decorator(func: DecoratedCallable) -> DecoratedCallable:  # type: ignore
            add_alternate_path(func)
            return add_path(func)

        return decorator
