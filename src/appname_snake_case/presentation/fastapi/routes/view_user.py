from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field

from appname_snake_case.application.view_user import ViewUser
from appname_snake_case.presentation.fastapi.cookies import UserDataCookie
from appname_snake_case.presentation.fastapi.schemas import (
    UserDataSchema,
    UserSchema,
)
from appname_snake_case.presentation.fastapi.tags import Tag


view_user_router = APIRouter()


class RegisterUserSchema(BaseModel):
    user_name: str = Field(alias="userName")


@view_user_router.get(
    "/user",
    responses={status.HTTP_200_OK: {"model": UserSchema}},
    summary="View user",
    description="View current user.",
    tags=[Tag.user],
)
@inject
async def view_user_route(
    view_user: FromDishka[ViewUser[str]],
    signed_user_data: UserDataCookie.StrOrNone = None,
) -> Response:
    result = await view_user(signed_user_data=signed_user_data)

    if result.user is None:
        user_data = None
    else:
        user_data = UserDataSchema(name=result.user.name)

    response_body_model = UserSchema(data=user_data)
    response_body = response_body_model.model_dump(by_alias=True)
    return JSONResponse(response_body)
