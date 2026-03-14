from pydantic import AliasPath, BaseModel, Field


class Downtime(BaseModel):
    id: str
    title: str
    comment: str = Field(validation_alias=AliasPath("extensions", "comment"))
    host_name: str = Field(validation_alias=AliasPath("extensions", "host_name"))
    is_service: str = Field(validation_alias=AliasPath("extensions", "is_service"))
    author: str = Field(validation_alias=AliasPath("extensions", "author"))
    start_time: str = Field(validation_alias=AliasPath("extensions", "start_time"))
    end_time: str = Field(validation_alias=AliasPath("extensions", "end_time"))
    recurring: str = Field(validation_alias=AliasPath("extensions", "recurring"))
