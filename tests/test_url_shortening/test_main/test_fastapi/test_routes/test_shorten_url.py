from fastapi import status
from httpx import AsyncClient
from pytest import mark
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from url_shortening.entities.shortened_url import ShortenedUrl


@mark.usefixtures("empty_postgres")
@mark.parametrize(
    "stage", [
        "response_status_code",
        "response_body",
    ]
)
async def test_ok(
    client: AsyncClient, stage: str, session: AsyncSession
) -> None:
    response = await client.post("/", json={"originalUrl": "https://google.com"})

    if stage == "response_status_code":
        assert response.status_code == status.HTTP_201_CREATED

    if stage == "response_body":
        async with session.begin():
            scalars = await session.scalars(select(ShortenedUrl))
        url = scalars.one()

        assert response.json() == {
            "shortenedUrlWithUuid": f"http://localhost:8000/{url.id.hex}",
            "shortenedUrlWithAlias": f"http://localhost:8000/{url.alias.text}?asAlias=true",
        }
