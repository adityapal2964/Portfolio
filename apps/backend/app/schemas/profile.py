import uuid

from pydantic import BaseModel, ConfigDict


class ProfileLinkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    kind: str
    label: str | None
    url: str
    sort_order: int


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    slug: str
    display_name: str
    headline: str | None
    location: str | None
    email: str | None
    avatar_url: str | None
    bio_short: str | None
    bio: str | None
    links: list[ProfileLinkResponse]
