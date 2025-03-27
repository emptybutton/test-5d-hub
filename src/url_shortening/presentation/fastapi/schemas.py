from typing import Self

from pydantic import BaseModel, Field

from url_shortening.infrastructure.adapters.shortened_url_reader import (
    ShortenedUrlView,
)


class NoDataSchema(BaseModel): ...


class ShortenedUrlSchema(BaseModel):
    shortened_url_with_uuid: str = Field(alias="shortenedUrlWithUuid")
    shortened_url_with_alias: str = Field(alias="shortenedUrlWithAlias")

    @classmethod
    def of(cls, view: ShortenedUrlView) -> "ShortenedUrlSchema":
        return ShortenedUrlSchema(
            shortenedUrlWithUuid=view.shortened_url_text_with_uuid,
            shortenedUrlWithAlias=view.shortened_url_text_with_alias,
        )


class ErrorListSchema[ErrorSchemaT](BaseModel):
    error_models: tuple[ErrorSchemaT] = Field(alias="errors")


class ErrorSchema(BaseModel):
    def to_list(self) -> ErrorListSchema[Self]:
        return ErrorListSchema(errors=(self,))
