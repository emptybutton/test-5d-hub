from typing import Literal, Self

from pydantic import BaseModel, Field


class NoDataSchema(BaseModel): ...


class UserDataSchema(BaseModel):
    name: str


class UserSchema(BaseModel):
    data: UserDataSchema | None


class ErrorListSchema[ErrorSchemaT](BaseModel):
    error_models: tuple[ErrorSchemaT] = Field(alias="errors")


class ErrorSchema(BaseModel):
    def to_list(self) -> ErrorListSchema[Self]:
        return ErrorListSchema(errors=(self,))


class AlreadyRegisteredUserErrorSchema(ErrorSchema):
    type: Literal["alreadyRegisteredUser"] = "alreadyRegisteredUser"
