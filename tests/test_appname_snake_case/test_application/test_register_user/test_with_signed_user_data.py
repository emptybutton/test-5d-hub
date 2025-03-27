from contextlib import suppress

from pytest import raises

from appname_snake_case.application.register_user import RegisterUser
from appname_snake_case.entities.core.user import (
    RegisteredUserToRegiterError,
    User,
)


async def test_result(
    register_user: RegisterUser[User | None], registered_user: User
) -> None:
    with raises(RegisteredUserToRegiterError):
        await register_user(signed_user_data=registered_user, user_name="Y")


async def test_users(
    register_user: RegisterUser[User | None], registered_user: User
) -> None:
    with suppress(Exception):
        await register_user(signed_user_data=registered_user, user_name="Y")

    assert not register_user.users
