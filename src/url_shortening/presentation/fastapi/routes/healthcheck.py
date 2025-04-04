from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response

from url_shortening.presentation.fastapi.schemas import NoDataSchema
from url_shortening.presentation.fastapi.tags import Tag


healthcheck_router = APIRouter()


@healthcheck_router.get(
    "/healthcheck",
    responses={status.HTTP_200_OK: {"model": NoDataSchema}},
    description="Checking if the server can accept requests.",
    tags=[Tag.monitoring],
)
def healthcheck() -> Response:
    return JSONResponse({})
