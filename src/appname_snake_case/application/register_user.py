from dataclasses import dataclass

from appname_snake_case.application.ports.user_data_signing import (
    UserDataSigning,
)
from appname_snake_case.application.ports.users import Users
from appname_snake_case.entities.core.user import registered_user_when


@dataclass(kw_only=True, frozen=True, slots=True)
class Output[SignedUserDataT]:
    signed_user_data: SignedUserDataT


@dataclass(kw_only=True, frozen=True, slots=True)
class RegisterUser[SignedUserDataT]:
    """
    :raises appname_snake_case.entities.user.RegisteredUserToRegiterError:
    """

    user_data_signing: UserDataSigning[SignedUserDataT]
    users: Users

    async def __call__(
        self, signed_user_data: SignedUserDataT | None, user_name: str
    ) -> Output[SignedUserDataT]:
        if signed_user_data is None:
            user = None
        else:
            user = await self.user_data_signing.user_when(
                signed_user_data=signed_user_data
            )

        registered_user = registered_user_when(user=user, user_name=user_name)

        await self.users.add(registered_user)

        signed_user_data = await self.user_data_signing.signed_user_data_when(
            user=registered_user
        )
        return Output(signed_user_data=signed_user_data)
