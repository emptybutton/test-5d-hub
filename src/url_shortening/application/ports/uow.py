from abc import ABC, abstractmethod

from url_shortening.entities.shortened_url import ShortenedUrl


type IdentifiedEntity = ShortenedUrl


class UoW(ABC):
    @abstractmethod
    async def register_new(self, entity: IdentifiedEntity, /) -> None: ...

    @abstractmethod
    async def register_dirty(self, entity: IdentifiedEntity, /) -> None: ...

    @abstractmethod
    async def register_deleted(self, entity: IdentifiedEntity, /) -> None: ...

    @abstractmethod
    async def commit(self) -> None: ...
