from abc import ABC, abstractmethod
from uuid import UUID

from appname_snake_case.entities.core.user import User


class Users(ABC):
    @abstractmethod
    async def add(self, user: User) -> None: ...

    @abstractmethod
    async def user_with_id(self, id: UUID) -> User | None: ...
