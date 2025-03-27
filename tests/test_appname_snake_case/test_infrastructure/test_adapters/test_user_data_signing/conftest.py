from uuid import UUID

from pytest import fixture

from appname_snake_case.entities.core.user import User


@fixture
def user() -> User:
    return User(id=UUID(int=1), name="X")
