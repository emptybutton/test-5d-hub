from collections.abc import Iterator

from fastapi import APIRouter

from url_shortening.presentation.fastapi.routes.healthcheck import (
    healthcheck_router,
)
from url_shortening.presentation.fastapi.routes.redirect_by_shortened_url import (  # noqa: E501
    redirect_by_shortened_url_router,
)
from url_shortening.presentation.fastapi.routes.shorten_url import (
    shorten_url_router,
)


all_routers = (
    healthcheck_router,
    shorten_url_router,
    redirect_by_shortened_url_router,
)


class UnknownRouterError(Exception): ...


def ordered(*routers: APIRouter) -> Iterator[APIRouter]:
    for router in all_routers:
        if router not in routers:
            raise UnknownRouterError

        yield router
