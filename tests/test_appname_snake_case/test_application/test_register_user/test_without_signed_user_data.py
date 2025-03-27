from dataclasses import asdict

from dirty_equals import IsUUID

from appname_snake_case.application.register_user import RegisterUser
from appname_snake_case.entities.core.user import User, unregistered_user


async def test_result(register_user: RegisterUser[User | None]) -> None:
    result = await register_user(
        signed_user_data=unregistered_user, user_name="Y"
    )
    assert result.signed_user_data is not None
    user_data = asdict(result.signed_user_data)

    assert user_data == dict(id=IsUUID(4), name="Y")


async def test_users(register_user: RegisterUser[User | None]) -> None:
    await register_user(signed_user_data=unregistered_user, user_name="Y")
    assert register_user.users
