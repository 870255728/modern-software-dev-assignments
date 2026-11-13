from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic import BaseModel, Field, field_validator


class NonBlankTextModel(BaseModel):
    @field_validator("*", mode="before")
    @classmethod
    def reject_blank_text(cls, value: object) -> object:
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("must not be blank")
        return value


class NoteCreate(NonBlankTextModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=10_000)


class NoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


class NotePatch(NonBlankTextModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, min_length=1, max_length=10_000)


class ActionItemCreate(NonBlankTextModel):
    description: str = Field(min_length=1, max_length=2_000)

class ActionItemCreate(BaseModel):
    description: str
    project_id: int | None = None


class ActionItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str
    completed: bool
    project_id: int | None
    created_at: datetime
    updated_at: datetime


class ActionItemPatch(NonBlankTextModel):
    description: str | None = Field(default=None, min_length=1, max_length=2_000)
    completed: bool | None = None
    project_id: int | None = None


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str = ""

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value


class ProjectPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value


class ProjectRead(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    action_items: list[ActionItemRead] = Field(default_factory=list)

    class Config:
        from_attributes = True
