from dataclasses import dataclass
from uuid import UUID

from url_shortening.application.ports.shortened_url_reader import (
    ShortenedUrlReader,
)


@dataclass(kw_only=True, frozen=True)
class ViewOriginalUrlByShortenedUrl[ShortenedUrlViewT, OriginalUrlViewT]:
    reader: ShortenedUrlReader[ShortenedUrlViewT, OriginalUrlViewT]

    async def __call__(
        self, text: str, use_alias: bool
    ) -> OriginalUrlViewT | None:
        if use_alias:
            return await (
                self.reader
                .read_original_url_by_shortened_url_alias_from_storage(text)
            )

        try:
            shortened_url_id = UUID(hex=text)
        except ValueError:
            return None

        return await (
            self.reader
            .read_original_url_by_shortened_url_id_from_storage(
                shortened_url_id
            )
        )
