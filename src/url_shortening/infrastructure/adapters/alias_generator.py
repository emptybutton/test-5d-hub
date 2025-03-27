from dataclasses import dataclass
from secrets import token_urlsafe

from url_shortening.application.ports.alias_generator import AliasGenerator
from url_shortening.entities.original_url import OriginalUrl
from url_shortening.entities.shortened_url import Alias


@dataclass(kw_only=True, frozen=True)
class TokenUrlsafeAsAliasGenerator(AliasGenerator):
    nbytes: int | None

    async def generate_alias(self, _: OriginalUrl, /) -> Alias:
        return Alias(text=token_urlsafe(self.nbytes))
