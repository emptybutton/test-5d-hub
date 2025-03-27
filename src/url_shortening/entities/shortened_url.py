from dataclasses import dataclass
from uuid import UUID

from url_shortening.entities.original_url import OriginalUrl


@dataclass(kw_only=True, frozen=True)
class Alias:
    text: str


@dataclass(kw_only=True)
class ShortenedUrl:
    id: UUID
    alias: Alias
    original_url: OriginalUrl
