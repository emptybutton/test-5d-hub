from typing import Annotated, Any

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query, status
from fastapi.params import Param
from fastapi.responses import JSONResponse, Response

from url_shortening.application.view_original_url_by_shortened_url import (
    ViewOriginalUrlByShortenedUrl,
)
from url_shortening.infrastructure.adapters.shortened_url_reader import (
    OriginalUrlView,
)
from url_shortening.presentation.fastapi.schemas import (
    NoDataSchema,
)
from url_shortening.presentation.fastapi.tags import Tag


redirect_by_shortened_url_router = APIRouter()


@redirect_by_shortened_url_router.get(
    "/{input_text}",
    responses={
        status.HTTP_307_TEMPORARY_REDIRECT: {
            "model": NoDataSchema,
            "headers": {
                "Location": {},
            },
        },
        status.HTTP_404_NOT_FOUND: {"model": NoDataSchema},
    },
    summary="Redirect by shortened URL",
    description="Redirect to original URL by shortened URL.",
    tags=[Tag.url],
)
@inject
async def redirect_by_shortened_url_route(
    view_original_url_by_shortened_url: FromDishka[
        ViewOriginalUrlByShortenedUrl[Any, OriginalUrlView | None]
    ],
    input_text: Annotated[str, Param(alias="input")],
    use_alias: Annotated[bool, Query(default=False, alias="alias")],
) -> Response:
    original_url_view = await view_original_url_by_shortened_url(
        input_text, use_alias
    )

    if original_url_view is None:
        return JSONResponse({}, status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse(
        {},
        headers={"Location": original_url_view.original_url_text},
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )
