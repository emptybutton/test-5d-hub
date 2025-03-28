from collections.abc import AsyncIterator

from fastapi import FastAPI
from httpx import AsyncClient
from httpx_ws.transport import ASGIWebSocketTransport
from pytest import fixture
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from url_shortening.infrastructure.sqlalchemy.tables import metadata
from url_shortening.main.fastapi.di import container
from url_shortening.presentation.fastapi.app import app_from


@fixture
async def app() -> FastAPI:
    return await app_from(container)


@fixture
async def session() -> AsyncIterator[AsyncSession]:
    async with container() as request_container:
        yield await request_container.get(AsyncSession)


@fixture
async def empty_postgres(session: AsyncSession) -> None:
    async with session.begin():
        for table in reversed(metadata.sorted_tables):
            await session.execute(text(f"TRUNCATE {table.name};"))

        await session.commit()


@fixture
def client(app: FastAPI) -> AsyncClient:
    transport = ASGIWebSocketTransport(app=app)

    return AsyncClient(transport=transport, base_url="http://localhost")
