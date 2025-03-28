from typing import Any

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field

from url_shortening.application.shorten_url import ShortenUrl
from url_shortening.infrastructure.adapters.shortened_url_reader import (
    ShortenedUrlView,
)
from url_shortening.presentation.fastapi.schemas import (
    ShortenedUrlSchema,
)
from url_shortening.presentation.fastapi.tags import Tag


shorten_url_router = APIRouter()


class ShortenUrlSchema(BaseModel):
    original_url: str = Field(alias="originalUrl")


@shorten_url_router.post(
    "/",
    responses={
        status.HTTP_201_CREATED: {"model": ShortenedUrlSchema},
    },
    summary="Shorten url",
    description="Shorten url to access it under alias or id.",
    tags=[Tag.url],
)
@inject
async def shorten_url_route(
    shorten_url: FromDishka[ShortenUrl[ShortenedUrlView, Any]],
    request_body: ShortenUrlSchema,
) -> Response:
    shortened_url_view = await shorten_url(request_body.original_url)

    response_body = (
        ShortenedUrlSchema
        .of(shortened_url_view)
        .model_dump(mode="json", by_alias=True)
    )
    return JSONResponse(response_body, status_code=status.HTTP_201_CREATED)
