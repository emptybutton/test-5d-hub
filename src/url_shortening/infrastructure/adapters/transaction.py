from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def create_postgres_transaction(
    session: AsyncSession
) -> AsyncIterator[None]:
    async with session.begin():
        yield
        await session.commit()
