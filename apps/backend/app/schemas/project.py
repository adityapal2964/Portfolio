import uuid
from datetime import date
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator


class ProjectLinkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    kind: str
    label: str | None
    url: str
    sort_order: int


class ProjectMediaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    kind: str
    url: str
    alt_text: str | None
    caption: str | None
    mime_type: str | None
    is_primary: bool
    sort_order: int


class SkillSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    slug: str
    name: str
    category: str | None


class CategorySummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    slug: str
    name: str


class TagSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    slug: str
    name: str


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    profile_id: uuid.UUID
    slug: str
    title: str
    summary: str | None
    body: str | None
    is_featured: bool
    sort_order: int
    started_on: date | None
    ended_on: date | None
    links: list[ProjectLinkResponse]
    media: list[ProjectMediaResponse]
    skills: list[SkillSummary]
    categories: list[CategorySummary]
    tags: list[TagSummary]

    @field_validator("skills", mode="before")
    @classmethod
    def unwrap_skills(cls, value: Any) -> Any:
        if not value:
            return []
        first = value[0]
        if hasattr(first, "skill"):
            return [item.skill for item in sorted(value, key=lambda item: item.sort_order)]
        return value

    @field_validator("categories", mode="before")
    @classmethod
    def unwrap_categories(cls, value: Any) -> Any:
        if not value:
            return []
        first = value[0]
        if hasattr(first, "category"):
            return [item.category for item in sorted(value, key=lambda item: item.sort_order)]
        return value

    @field_validator("tags", mode="before")
    @classmethod
    def unwrap_tags(cls, value: Any) -> Any:
        if not value:
            return []
        first = value[0]
        if hasattr(first, "tag"):
            return [item.tag for item in value]
        return value
