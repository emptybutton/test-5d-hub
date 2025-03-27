from uuid import UUID

from pytest import fixture
from sqlalchemy import exists, insert, select
from sqlalchemy.ext.asyncio import AsyncConnection

from appname_snake_case.entities.core.user import User
from appname_snake_case.infrastructure.adapters.users import InPostgresUsers
from appname_snake_case.infrastructure.sqlalchemy.tables import user_table


@fixture
def user1() -> User:
    return User(id=UUID(int=1), name="X")


@fixture
def user2() -> User:
    return User(id=UUID(int=2), name="Y")


@fixture
def no_users(postgres_connection: AsyncConnection) -> InPostgresUsers:
    return InPostgresUsers(_connection=postgres_connection)


@fixture
async def users(postgres_connection: AsyncConnection) -> InPostgresUsers:
    stmt = insert(user_table).values(id=UUID(int=1), name="X")
    await postgres_connection.execute(stmt)

    return InPostgresUsers(_connection=postgres_connection)


async def test_no_users_add(
    postgres_connection: AsyncConnection, no_users: InPostgresUsers, user1: User
) -> None:
    await no_users.add(user1)

    stmt = select(
        exists(user_table).where(
            user_table.c.id == user1.id,
            user_table.c.name == user1.name,
        )
    )
    assert await postgres_connection.scalar(stmt)


async def test_users_add(
    postgres_connection: AsyncConnection,
    users: InPostgresUsers,
    user1: User,
    user2: User,
) -> None:
    await users.add(user2)

    user2_stmt = select(
        exists(user_table).where(
            user_table.c.id == user2.id,
            user_table.c.name == user2.name,
        )
    )
    user1_stmt = select(
        exists(user_table).where(
            user_table.c.id == user1.id,
            user_table.c.name == user1.name,
        )
    )
    is_user1_in_users = await postgres_connection.scalar(user1_stmt)
    is_user2_in_users = await postgres_connection.scalar(user2_stmt)

    assert is_user1_in_users and is_user2_in_users


async def test_user_with_id_when_user_exists(
    users: InPostgresUsers, user1: User
) -> None:
    user = await users.user_with_id(UUID(int=1))

    assert user == user1


async def test_user_with_id_when_no_user(no_users: InPostgresUsers) -> None:
    user = await no_users.user_with_id(UUID(int=1))

    assert user is None
