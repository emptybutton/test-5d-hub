from dataclasses import asdict
from uuid import UUID

from dirty_equals import IsUUID
from pytest import fixture, raises

from appname_snake_case.entities.core.user import (
    RegisteredUserToRegiterError,
    User,
    registered_user_when,
    unregistered_user,
)


@fixture
def registered_user() -> User:
    return User(id=UUID(int=0), name="X")


def test_registered_user_when_user_is_unregistered() -> None:
    user = registered_user_when(user=unregistered_user, user_name="Y")
    user_data = asdict(user)

    assert user_data == dict(id=IsUUID(4), name="Y")


def test_registered_user_when_user_is_registered(registered_user: User) -> None:
    with raises(RegisteredUserToRegiterError):
        registered_user_when(user=registered_user, user_name="Y")
