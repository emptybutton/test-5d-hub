from fastapi import status
from httpx import AsyncClient
from pytest import mark


@mark.parametrize("stage", ["status_code", "body", "cookies"])
async def test_ok(client: AsyncClient, stage: str) -> None:
    response = await client.post("/user", json={"userName": "X"})

    if stage == "status_code":
        assert response.status_code == status.HTTP_201_CREATED

    if stage == "body":
        assert response.json() == {}

    if stage == "cookies":
        assert set(response.cookies) == {"userData"}
