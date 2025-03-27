from dishka import Provider, Scope, make_async_container, provide

from appname_snake_case.entrypoint.common.di import (
    ApplicationProvider,
    InfrastructureProvider,
)
from appname_snake_case.presentation.fastapi.app import (
    FastAPIAppCoroutines,
    FastAPIAppRouters,
)
from appname_snake_case.presentation.fastapi.routers import all_routers


class WebServiceProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_routers(self) -> FastAPIAppRouters:
        return all_routers

    @provide
    def provide_coroutines(self) -> FastAPIAppCoroutines:
        return []


container = make_async_container(
    WebServiceProvider(),
    InfrastructureProvider(),
    ApplicationProvider(),
)
