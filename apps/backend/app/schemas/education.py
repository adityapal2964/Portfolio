import uuid
from datetime import date

from pydantic import BaseModel, ConfigDict


class EducationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    profile_id: uuid.UUID
    institution: str
    degree: str | None
    field_of_study: str | None
    location: str | None
    start_date: date | None
    end_date: date | None
    summary: str | None
    body: str | None
    sort_order: int
