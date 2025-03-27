from dataclasses import dataclass, field
from uuid import UUID

import jwt

from appname_snake_case.application.ports.user_data_signing import (
    UserDataSigning,
)
from appname_snake_case.entities.core.user import User
from appname_snake_case.infrastructure.types import JWT


@dataclass(kw_only=True, frozen=True, slots=True)
class UserDataSigningAsIdentification(UserDataSigning[User | None]):
    async def signed_user_data_when(self, *, user: User) -> User | None:
        return user

    async def user_when(self, *, signed_user_data: User | None) -> User | None:
        return signed_user_data


@dataclass(kw_only=True, frozen=True, slots=True)
class UserDataSigningToHS256JWT(UserDataSigning[JWT]):
    secret: str = field(repr=False)

    async def signed_user_data_when(self, *, user: User) -> JWT:
        mapping = {"id": user.id.hex, "name": user.name}

        return jwt.encode(mapping, self.secret, algorithm="HS256")

    async def user_when(self, *, signed_user_data: JWT) -> User | None:
        token = signed_user_data

        try:
            user_data = jwt.decode(token, self.secret, algorithms="HS256")
        except jwt.DecodeError:
            return None

        user_id_hex: str | None = user_data.get("id")
        user_name: str | None = user_data.get("name")

        if user_id_hex is None or user_name is None:
            return None

        try:
            user_id = UUID(hex=user_id_hex)
        except ValueError:
            return None

        return User(id=user_id, name=user_name)
