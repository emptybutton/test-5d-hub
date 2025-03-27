from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field

from appname_snake_case.application.register_user import RegisterUser
from appname_snake_case.entities.core.user import RegisteredUserToRegiterError
from appname_snake_case.presentation.fastapi.cookies import UserDataCookie
from appname_snake_case.presentation.fastapi.schemas import (
    AlreadyRegisteredUserErrorSchema,
    ErrorListSchema,
    NoDataSchema,
)
from appname_snake_case.presentation.fastapi.tags import Tag


register_user_router = APIRouter()


class RegisterUserSchema(BaseModel):
    user_name: str = Field(alias="userName")


@register_user_router.post(
    "/user",
    responses={
        status.HTTP_201_CREATED: {"model": NoDataSchema},
        status.HTTP_409_CONFLICT: {
            "model": ErrorListSchema[AlreadyRegisteredUserErrorSchema]
        },
    },
    summary="Register user",
    description="Register current user.",
    tags=[Tag.user],
)
@inject
async def register_user_route(
    register_user: FromDishka[RegisterUser[str]],
    request_body: RegisterUserSchema,
    signed_user_data: UserDataCookie.StrOrNone = None,
) -> Response:
    try:
        result = await register_user(
            signed_user_data=signed_user_data, user_name=request_body.user_name
        )
    except RegisteredUserToRegiterError:
        response_body_model = AlreadyRegisteredUserErrorSchema().to_list()
        response_body = response_body_model.model_dump(by_alias=True)
        return JSONResponse(response_body, status_code=status.HTTP_409_CONFLICT)

    response = JSONResponse({}, status_code=status.HTTP_201_CREATED)
    cookie = UserDataCookie(response)
    cookie.set(result.signed_user_data)

    return response
