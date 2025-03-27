from dataclasses import dataclass
from typing import TypeGuard
from uuid import UUID, uuid4


@dataclass(kw_only=True, frozen=True, slots=True)
class User:
    id: UUID
    name: str


type RegisteredUser = User
type UnregisteredUser = None
type AnyUser = RegisteredUser | UnregisteredUser


unregistered_user: UnregisteredUser = None


def is_registered(user: AnyUser) -> TypeGuard[RegisteredUser]:
    return user is not None


class RegisteredUserToRegiterError(Exception): ...


def registered_user_when(*, user: AnyUser, user_name: str) -> User:
    """
    :raises appname_snake_case.entities.user.RegisteredUserToRegiterError:
    """

    if is_registered(user):
        raise RegisteredUserToRegiterError

    return User(id=uuid4(), name=user_name)
