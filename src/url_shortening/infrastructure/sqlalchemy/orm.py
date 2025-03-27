from typing import cast

from sqlalchemy.orm import composite, registry

from url_shortening.entities.original_url import OriginalUrl
from url_shortening.entities.shortened_url import Alias, ShortenedUrl
from url_shortening.infrastructure.sqlalchemy.tables import (
    metadata,
    shortened_url_table,
)


mapper_registry = registry(metadata=metadata)

mapper_registry.map_imperatively(
    ShortenedUrl,
    shortened_url_table,
    properties=dict(
        id=shortened_url_table.c.id,
        alias=composite(lambda text: Alias(text=cast(str, text))),
        original_url=composite(
            lambda text: OriginalUrl(text=cast(str, text)),
            shortened_url_table.c.original_url_text,
        )
    ),
)
