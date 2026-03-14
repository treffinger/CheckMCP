from pydantic import AliasPath, BaseModel, Field


class Folder(BaseModel):
    name: str = Field(validation_alias="title")
    path: str = Field(validation_alias=AliasPath("extensions", "path"))
    created_at: str = Field(validation_alias=AliasPath("extensions", "attributes", "meta_data", "created_at"))
    updated_at: str = Field(validation_alias=AliasPath("extensions", "attributes", "meta_data", "updated_at"))
