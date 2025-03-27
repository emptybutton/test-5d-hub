from abc import ABC, abstractmethod
from uuid import UUID

from url_shortening.entities.shortened_url import ShortenedUrl


class ShortenedUrlReader[ShortenedUrlViewT, OriginalUrlViewT](ABC):
    @abstractmethod
    async def read_original_url_by_shortened_url_id_from_storage(
        self,
        shortened_url_id: UUID,
        /,
    ) -> OriginalUrlViewT | None: ...

    @abstractmethod
    async def read_original_url_by_shortened_url_alias_from_storage(
        self,
        shortened_url_alias_text: str,
        /,
    ) -> OriginalUrlViewT | None: ...

    @abstractmethod
    async def read_shortened_url(
        self,
        shortened_url: ShortenedUrl,
        /,
    ) -> ShortenedUrlViewT: ...
