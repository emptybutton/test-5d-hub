from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    create_async_engine,
)

from appname_snake_case.application.ports.user_data_signing import (
    UserDataSigning,
)
from appname_snake_case.application.ports.users import Users
from appname_snake_case.application.register_user import RegisterUser
from appname_snake_case.application.view_user import ViewUser
from appname_snake_case.infrastructure.adapters.user_data_signing import (
    UserDataSigningToHS256JWT,
)
from appname_snake_case.infrastructure.adapters.users import InPostgresUsers
from appname_snake_case.infrastructure.envs import RuntimeEnvs


type PostgresEngine = AsyncEngine
type PostgresConnection = AsyncConnection


class InfrastructureProvider(Provider):
    scope = Scope.APP

    provide_runtime_envs = provide(source=RuntimeEnvs.load)

    @provide
    async def provide_postgres_engine(
        self, envs: RuntimeEnvs
    ) -> PostgresEngine:
        return create_async_engine(envs.postgres_url)

    @provide(scope=Scope.REQUEST)
    async def provide_postgres_connection(
        self, engine: PostgresEngine
    ) -> AsyncIterator[PostgresConnection]:
        async with engine.connect() as connection:
            yield connection

    @provide
    def provide_user_data_signing(
        self, envs: RuntimeEnvs
    ) -> UserDataSigning[str]:
        return UserDataSigningToHS256JWT(secret=envs.jwt_secret)

    @provide(scope=Scope.REQUEST)
    def provide_users(self, connection: PostgresConnection) -> Users:
        return InPostgresUsers(_connection=connection)


class ApplicationProvider(Provider):
    scope = Scope.REQUEST

    provide_register_user = provide(RegisterUser[str])
    provide_view_user = provide(ViewUser[str])
