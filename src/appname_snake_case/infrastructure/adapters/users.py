from collections.abc import Iterator
from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncConnection

from appname_snake_case.application.ports.users import Users
from appname_snake_case.entities.core.user import User
from appname_snake_case.infrastructure.sqlalchemy.tables import user_table


@dataclass(kw_only=True, frozen=True, slots=True, unsafe_hash=False)
class InMemoryUsers(Users):
    _user_set: set[User]

    def __iter__(self) -> Iterator[User]:
        return iter(set(self._user_set))

    def __bool__(self) -> bool:
        return bool(self._user_set)

    async def add(self, user: User) -> None:
        self._user_set.add(user)

    async def user_with_id(self, id: UUID) -> User | None:
        for user in self._user_set:
            if user.id == id:
                return user

        return None


@dataclass(kw_only=True, frozen=True, slots=True)
class InPostgresUsers(Users):
    _connection: AsyncConnection

    async def add(self, user: User) -> None:
        stmt = insert(user_table).values(id=user.id, name=user.name)
        await self._connection.execute(stmt)

    async def user_with_id(self, id: UUID) -> User | None:
        stmt = select(user_table.c.name).where(user_table.c.id == id)
        rows = await self._connection.execute(stmt)
        row = rows.first()

        if row is None:
            return None

        return User(id=id, name=row.name)
