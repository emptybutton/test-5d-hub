from abc import ABC, abstractmethod

from url_shortening.entities.original_url import OriginalUrl
from url_shortening.entities.shortened_url import Alias


class AliasGenerator(ABC):
    @abstractmethod
    async def generate_alias(self, url: OriginalUrl, /) -> Alias: ...
