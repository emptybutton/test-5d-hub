from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from url_shortening.application.ports.shortened_url_reader import (
    ShortenedUrlReader,
)
from url_shortening.entities.shortened_url import ShortenedUrl
from url_shortening.infrastructure.sqlalchemy.tables import shortened_url_table


@dataclass(kw_only=True, frozen=True)
class OriginalUrlView:
    original_url_text: str


@dataclass(kw_only=True, frozen=True)
class ShortenedUrlView:
    shortened_url_text_with_uuid: str
    shortened_url_text_with_alias: str


@dataclass(kw_only=True, frozen=True)
class ShortenedUrlReaderFromPostgres(
    ShortenedUrlReader[ShortenedUrlView, OriginalUrlView]
):
    session: AsyncSession
    shortened_url_prefix: str

    def __post_init__(self) -> None:
        assert not self.shortened_url_prefix.endswith("/")

    async def read_original_url_by_shortened_url_id_from_storage(
        self,
        shortened_url_id: UUID,
        /,
    ) -> OriginalUrlView | None:
        stmt: Select[tuple[str]] = (
            select(shortened_url_table.c.original_url_text)
            .where(shortened_url_table.c.id == shortened_url_id)
        )
        original_url_text = await self.session.scalar(stmt)

        if original_url_text is None:
            return None

        return OriginalUrlView(original_url_text=original_url_text)

    async def read_original_url_by_shortened_url_alias_from_storage(
        self,
        shortened_url_alias_text: str,
        /,
    ) -> OriginalUrlView | None:
        stmt: Select[tuple[str]] = (
            select(shortened_url_table.c.original_url_text)
            .where(shortened_url_table.c.alias_text == shortened_url_alias_text)
        )
        original_url_text = await self.session.scalar(stmt)

        if original_url_text is None:
            return None

        return OriginalUrlView(original_url_text=original_url_text)

    async def read_shortened_url(
        self,
        shortened_url: ShortenedUrl,
        /,
    ) -> ShortenedUrlView:
        return ShortenedUrlView(
            shortened_url_text_with_uuid=(
                self._create_shortened_url_text_with_id(shortened_url)
            ),
            shortened_url_text_with_alias=(
                self._create_shortened_url_text_with_alias(shortened_url)
            ),
        )

    def _create_shortened_url_text_with_id(
        self, shortened_url: ShortenedUrl
    ) -> str:
        return f"{self.shortened_url_prefix}/{shortened_url.id.hex}"

    def _create_shortened_url_text_with_alias(
        self, shortened_url: ShortenedUrl
    ) -> str:
        return f"{self.shortened_url_prefix}/{shortened_url.alias}?alias=true"
