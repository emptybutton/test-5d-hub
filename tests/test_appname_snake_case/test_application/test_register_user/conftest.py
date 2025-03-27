from uuid import UUID

from pytest import fixture

from appname_snake_case.application.register_user import RegisterUser
from appname_snake_case.entities.core.user import User
from appname_snake_case.infrastructure.adapters.user_data_signing import (
    UserDataSigningAsIdentification,
)
from appname_snake_case.infrastructure.adapters.users import InMemoryUsers


@fixture
def register_user() -> RegisterUser[User | None]:
    return RegisterUser(
        user_data_signing=UserDataSigningAsIdentification(),
        users=InMemoryUsers(_user_set=set()),
    )


@fixture
def registered_user() -> User:
    return User(id=UUID(int=0), name="X")
