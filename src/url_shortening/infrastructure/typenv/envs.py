from dataclasses import dataclass

import typenv


@dataclass(kw_only=True, frozen=True, slots=True)
class Envs:
    postgres_url: str
    public_url: str
    shortened_url_alias_lenght: int

    @classmethod
    def load(cls) -> "Envs":
        loader = typenv.Env()

        return Envs(
            postgres_url=loader.str("POSTGRES_URL"),
            public_url=loader.str("PUBLIC_URL"),
            shortened_url_alias_lenght=loader.int("SHORTENED_URL_ALIAS_LENGHT"),
        )
