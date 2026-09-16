import uuid
from datetime import date

from pydantic import BaseModel, ConfigDict


class AchievementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    profile_id: uuid.UUID
    title: str
    url: str | None
    occurred_on: date | None
    summary: str | None
    body: str | None
    sort_order: int
