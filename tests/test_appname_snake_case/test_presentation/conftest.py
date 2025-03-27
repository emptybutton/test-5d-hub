from dishka import AsyncContainer, Provider, Scope, make_async_container
from pytest import fixture

from appname_snake_case.application.ports.user_data_signing import (
    UserDataSigning,
)
from appname_snake_case.application.ports.users import Users
from appname_snake_case.application.register_user import RegisterUser
from appname_snake_case.application.view_user import ViewUser
from appname_snake_case.infrastructure.adapters.user_data_signing import (
    UserDataSigningToHS256JWT,
)
from appname_snake_case.infrastructure.adapters.users import InMemoryUsers


@fixture
def container() -> AsyncContainer:
    provider = Provider(scope=Scope.APP)

    provider.provide(
        lambda: UserDataSigningToHS256JWT(secret="super secret secret"),
        provides=UserDataSigning[str],
    )
    provider.provide(lambda: InMemoryUsers(_user_set=set()), provides=Users)
    provider.provide(RegisterUser[str])
    provider.provide(ViewUser[str])

    return make_async_container(provider)
