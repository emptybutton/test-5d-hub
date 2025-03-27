from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class OriginalUrl:
    text: str
