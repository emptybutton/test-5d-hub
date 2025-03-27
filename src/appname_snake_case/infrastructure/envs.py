from dataclasses import dataclass

import typenv


@dataclass(kw_only=True, frozen=True, slots=True)
class RuntimeEnvs:
    jwt_secret: str
    postgres_url: str

    @classmethod
    def load(cls) -> "RuntimeEnvs":
        loader = typenv.Env()

        return RuntimeEnvs(
            jwt_secret=loader.str("JWT_SECRET"),
            postgres_url=loader.str("POSTGRES_URL"),
        )


@dataclass(kw_only=True, frozen=True, slots=True)
class AlembicEnvs:
    postgres_url: str

    @classmethod
    def load(cls) -> "AlembicEnvs":
        loader = typenv.Env()

        return AlembicEnvs(postgres_url=loader.str("POSTGRES_URL"))


@dataclass(kw_only=True, frozen=True, slots=True)
class TestsEnvs:
    postgres_url: str

    @classmethod
    def load(cls) -> "TestsEnvs":
        loader = typenv.Env()

        return TestsEnvs(postgres_url=loader.str("POSTGRES_URL"))
