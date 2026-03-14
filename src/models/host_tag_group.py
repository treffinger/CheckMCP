from pydantic import AliasPath, BaseModel, Field

from .tag import Tag


class HostTagGroup(BaseModel):
    name: str = Field(validation_alias="id")
    title: str = Field(validation_alias="title")
    tags: list[Tag] = Field(validation_alias=AliasPath("extensions", "tags"))
