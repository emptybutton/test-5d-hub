from dataclasses import dataclass
from uuid import uuid4

from url_shortening.application.ports.alias_generator import AliasGenerator
from url_shortening.application.ports.shortened_url_reader import (
    ShortenedUrlReader,
)
from url_shortening.application.ports.transaction import Transaction
from url_shortening.application.ports.uow import UoW
from url_shortening.entities.original_url import OriginalUrl
from url_shortening.entities.shortened_url import ShortenedUrl


@dataclass(kw_only=True, frozen=True)
class ShortenUrl[ShortenedUrlViewT, OriginalUrlViewT]:
    uow: UoW
    transaction: Transaction
    reader: ShortenedUrlReader[ShortenedUrlViewT, OriginalUrlViewT]
    alias_generator: AliasGenerator

    async def __call__(self, original_url_text: str) -> ShortenedUrlViewT:
        original_url = OriginalUrl(text=original_url_text)
        alias = await self.alias_generator.generate_alias(original_url)

        shortened_url = ShortenedUrl(
            id=uuid4(), alias=alias, original_url=original_url
        )

        async with self.transaction:
            await self.uow.register_new(shortened_url)
            await self.uow.commit()

            return await self.reader.read_shortened_url(shortened_url)
