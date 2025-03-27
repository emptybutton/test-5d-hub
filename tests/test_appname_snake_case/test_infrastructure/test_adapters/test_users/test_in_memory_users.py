from uuid import UUID

from pytest import fixture

from appname_snake_case.entities.core.user import User
from appname_snake_case.infrastructure.adapters.users import InMemoryUsers


@fixture
def user1() -> User:
    return User(id=UUID(int=1), name="X")


@fixture
def user2() -> User:
    return User(id=UUID(int=2), name="Y")


@fixture
def no_users() -> InMemoryUsers:
    return InMemoryUsers(_user_set=set())


@fixture
def users(user1: User) -> InMemoryUsers:
    return InMemoryUsers(_user_set={user1})


async def test_no_users_add(no_users: InMemoryUsers, user1: User) -> None:
    await no_users.add(user1)

    assert set(no_users) == {user1}


async def test_users_add(
    users: InMemoryUsers, user1: User, user2: User
) -> None:
    await users.add(user2)

    assert set(users) == {user1, user2}


async def test_user_with_id_when_user_exists(
    users: InMemoryUsers, user1: User
) -> None:
    user = await users.user_with_id(UUID(int=1))

    assert user == user1


async def test_user_with_id_when_no_user(no_users: InMemoryUsers) -> None:
    user = await no_users.user_with_id(UUID(int=1))

    assert user is None
