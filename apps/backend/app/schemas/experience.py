import uuid
from datetime import date
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator

from app.schemas.skill import SkillResponse


class ExperienceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    profile_id: uuid.UUID
    company_name: str
    company_url: str | None
    title: str
    location: str | None
    employment_type: str | None
    start_date: date | None
    end_date: date | None
    is_current: bool
    summary: str | None
    body: str | None
    sort_order: int
    skills: list[SkillResponse]

    @field_validator("skills", mode="before")
    @classmethod
    def unwrap_skills(cls, value: Any) -> Any:
        if not value:
            return []
        first = value[0]
        if hasattr(first, "skill"):
            return [item.skill for item in sorted(value, key=lambda item: item.sort_order)]
        return value
