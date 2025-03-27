from collections.abc import AsyncIterator
from typing import Any

from dishka import AnyOf, Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from url_shortening.application.ports.alias_generator import AliasGenerator
from url_shortening.application.ports.shortened_url_reader import (
    ShortenedUrlReader,
)
from url_shortening.application.ports.transaction import Transaction
from url_shortening.application.ports.uow import UoW
from url_shortening.application.shorten_url import ShortenUrl
from url_shortening.application.view_original_url_by_shortened_url import (
    ViewOriginalUrlByShortenedUrl,
)
from url_shortening.infrastructure.adapters.alias_generator import (
    TokenUrlsafeAsAliasGenerator,
)
from url_shortening.infrastructure.adapters.shortened_url_reader import (
    OriginalUrlView,
    ShortenedUrlReaderFromPostgres,
    ShortenedUrlView,
)
from url_shortening.infrastructure.adapters.transaction import (
    create_postgres_transaction,
)
from url_shortening.infrastructure.adapters.uow import PostgresUoW
from url_shortening.infrastructure.typenv.envs import Envs


class ApplicationProvider(Provider):
    provide_envs = provide(source=Envs.load, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def provide_postgres_engine(
        self, envs: Envs
    ) -> AsyncEngine:
        return create_async_engine(envs.postgres_url)

    @provide(scope=Scope.REQUEST)
    async def provide_postgres_session(
        self, engine: AsyncEngine
    ) -> AsyncIterator[AsyncSession]:
        session = AsyncSession(
            engine, autoflush=False, autobegin=False, expire_on_commit=False
        )
        async with session:
            yield session

    @provide(scope=Scope.REQUEST)
    def provide_uow(self, session: AsyncSession) -> AnyOf[PostgresUoW, UoW]:
        return PostgresUoW(session=session)

    @provide(scope=Scope.REQUEST)
    def provide_transaction(self, session: AsyncSession) -> Transaction:
        return create_postgres_transaction(session)

    @provide(scope=Scope.REQUEST)
    def provide_shortened_url_reader(
        self, session: AsyncSession, envs: Envs
    ) -> AnyOf[
        ShortenedUrlReaderFromPostgres,
        ShortenedUrlReader[ShortenedUrlView, OriginalUrlView],
    ]:
        return ShortenedUrlReaderFromPostgres(
            shortened_url_prefix=envs.public_url,
            session=session,
        )

    @provide(scope=Scope.REQUEST)
    def provide_alias_generator(self, envs: Envs) -> AnyOf[
        TokenUrlsafeAsAliasGenerator,
        AliasGenerator,
    ]:
        return TokenUrlsafeAsAliasGenerator(
            nbytes=envs.shortened_url_alias_lenght
        )

    provide_shorten_url = provide(
        ShortenUrl[ShortenedUrlView, OriginalUrlView],
        scope=Scope.REQUEST,
        provides=AnyOf[
            ShortenUrl[ShortenedUrlView, OriginalUrlView],
            ShortenUrl[ShortenedUrlView, Any],
            ShortenUrl[Any, OriginalUrlView],
        ]
    )
    rovide_shorten_url = provide(
        ViewOriginalUrlByShortenedUrl[ShortenedUrlView, OriginalUrlView],
        scope=Scope.REQUEST,
        provides=AnyOf[
            ViewOriginalUrlByShortenedUrl[ShortenedUrlView, OriginalUrlView],
            ViewOriginalUrlByShortenedUrl[ShortenedUrlView, Any],
            ViewOriginalUrlByShortenedUrl[Any, OriginalUrlView],
        ]
    )
