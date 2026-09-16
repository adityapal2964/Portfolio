import uuid
from datetime import date

from pydantic import BaseModel, ConfigDict


class CertificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    profile_id: uuid.UUID
    name: str
    issuer: str
    issued_on: date | None
    expires_on: date | None
    credential_id: str | None
    credential_url: str | None
    sort_order: int
