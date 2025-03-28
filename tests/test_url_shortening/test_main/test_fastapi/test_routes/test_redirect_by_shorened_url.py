from uuid import UUID

from fastapi import status
from httpx import AsyncClient
from pytest import fixture, mark
from sqlalchemy.ext.asyncio import AsyncSession

from url_shortening.entities.original_url import OriginalUrl
from url_shortening.entities.shortened_url import Alias, ShortenedUrl


@fixture
def url0() -> ShortenedUrl:
    return ShortenedUrl(
        id=UUID(int=0),
        alias=Alias(text="X"),
        original_url=OriginalUrl(text="https://goooool.com"),
    )


@fixture
async def postgres_with_url0_only(
    session: AsyncSession, url0: ShortenedUrl, empty_postgres: None  # noqa: ARG001
) -> None:
    async with session.begin():
        session.add(url0)
        await session.commit()


@mark.usefixtures("postgres_with_url0_only")
@mark.parametrize(
    "stage", [
        "response_status_code",
        "response_headers",
    ]
)
async def test_with_stored_url_id(
    client: AsyncClient,
    stage: str,
    postgres_with_url0_only: None,  # noqa: ARG001
) -> None:
    response = await client.get("/00000000000000000000000000000000")

    if stage == "response_status_code":
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT

    if stage == "response_headers":
        assert response.headers["Location"] == "https://goooool.com"


@mark.parametrize(
    "stage", [
        "response_status_code",
        "response_headers",
    ]
)
async def test_with_stored_url_alias(
    client: AsyncClient,
    stage: str,
    postgres_with_url0_only: None,  # noqa: ARG001
) -> None:
    response = await client.get("/X?asAlias=true")

    if stage == "response_status_code":
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT

    if stage == "response_headers":
        assert response.headers["Location"] == "https://goooool.com"


async def test_with_unstored_url_id(
    client: AsyncClient,
    empty_postgres: None,  # noqa: ARG001
) -> None:
    response = await client.get("/00000000000000000000000000000000")

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_with_unstored_url_alias(
    client: AsyncClient,
    empty_postgres: None,  # noqa: ARG001
) -> None:
    response = await client.get("/X?asAlias=true")

    assert response.status_code == status.HTTP_404_NOT_FOUND
