from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from url_shortening.application.ports.uow import UoW
from url_shortening.entities.shortened_url import ShortenedUrl


type IdentifiedEntity = ShortenedUrl


@dataclass(kw_only=True, frozen=True)
class PostgresUoW(UoW):
    session: AsyncSession

    async def register_new(self, entity: IdentifiedEntity) -> None:
        self.session.add(entity)

    async def register_dirty(self, entity: IdentifiedEntity) -> None: ...

    async def register_deleted(self, entity: IdentifiedEntity) -> None:
        await self.session.delete(entity)

    async def commit(self) -> None:
        await self.session.flush()
