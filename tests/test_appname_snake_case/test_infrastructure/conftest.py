from collections.abc import AsyncIterable

from pytest import fixture
from sqlalchemy import NullPool, delete
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    create_async_engine,
)

from appname_snake_case.infrastructure.envs import TestsEnvs
from appname_snake_case.infrastructure.sqlalchemy.tables import metadata


@fixture(scope="session")
def postgres_engine(envs: TestsEnvs) -> AsyncEngine:
    return create_async_engine(envs.postgres_url, poolclass=NullPool)


@fixture(scope="session")
async def _session_postgres_connection(
    postgres_engine: AsyncEngine,
) -> AsyncIterable[AsyncConnection]:
    async with postgres_engine.connect() as connection:
        yield connection


@fixture()
async def postgres_connection(
    _session_postgres_connection: AsyncConnection,
) -> AsyncConnection:
    await _clear_db(_session_postgres_connection)
    return _session_postgres_connection


async def _clear_db(connection: AsyncConnection) -> None:
    for table in reversed(metadata.sorted_tables):
        await connection.execute(delete(table))
