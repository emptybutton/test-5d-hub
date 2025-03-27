from dishka import Provider, Scope, make_async_container, provide

from url_shortening.main.common.di import ApplicationProvider
from url_shortening.presentation.fastapi.app import FastAPIAppRouters
from url_shortening.presentation.fastapi.routers import all_routers


class FastAPIProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_routers(self) -> FastAPIAppRouters:
        return all_routers


container = make_async_container(
    FastAPIProvider(),
    ApplicationProvider(),
)
