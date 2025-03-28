from dataclasses import dataclass
from uuid import UUID

from url_shortening.application.ports.shortened_url_reader import (
    ShortenedUrlReader,
)
from url_shortening.application.ports.transaction import Transaction


@dataclass(kw_only=True, frozen=True)
class ViewOriginalUrlByShortenedUrl[ShortenedUrlViewT, OriginalUrlViewT]:
    reader: ShortenedUrlReader[ShortenedUrlViewT, OriginalUrlViewT]
    transaction: Transaction

    async def __call__(
        self, shortened_url_part: str, is_shortened_url_with_alias: bool
    ) -> OriginalUrlViewT | None:
        if is_shortened_url_with_alias:
            async with self.transaction:
                alias_text = shortened_url_part
                return await (
                    self.reader
                    .read_original_url_by_shortened_url_alias_from_storage(
                        alias_text
                    )
                )

        try:
            shortened_url_id = UUID(hex=shortened_url_part)
        except ValueError:
            return None

        async with self.transaction:
            return await (
                self.reader
                .read_original_url_by_shortened_url_id_from_storage(
                    shortened_url_id
                )
            )
