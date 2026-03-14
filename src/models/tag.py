from pydantic import BaseModel, Field


class Tag(BaseModel):
    name: str = Field(validation_alias="id")
    title: str
