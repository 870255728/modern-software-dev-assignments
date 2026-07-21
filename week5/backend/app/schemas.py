from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, field_validator


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=10_000)


class NoteUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=10_000)


class NoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str


class ActionItemCreate(BaseModel):
    description: str


class ActionItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str
    completed: bool


class ActionItemsBulkComplete(BaseModel):
    ids: Annotated[list[PositiveInt], Field(min_length=1)]

    @field_validator("ids")
    @classmethod
    def ids_must_be_unique(cls, ids: list[int]) -> list[int]:
        if len(ids) != len(set(ids)):
            raise ValueError("Action item IDs must be unique")
        return ids
