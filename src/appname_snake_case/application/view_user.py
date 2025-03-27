from dataclasses import dataclass

from appname_snake_case.application.ports.user_data_signing import (
    UserDataSigning,
)
from appname_snake_case.entities.core.user import User


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    user: User | None


@dataclass(kw_only=True, frozen=True, slots=True)
class ViewUser[SignedUserDataT]:
    user_data_signing: UserDataSigning[SignedUserDataT]

    async def __call__(
        self, signed_user_data: SignedUserDataT | None
    ) -> Output:
        if signed_user_data is None:
            return Output(user=None)

        user = await self.user_data_signing.user_when(
            signed_user_data=signed_user_data
        )

        return Output(user=user)
