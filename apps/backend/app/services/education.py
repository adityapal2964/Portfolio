import uuid

from sqlalchemy.orm import Session

from app.models.education import Education
from app.repositories.education import EducationRepository
from app.repositories.profile import ProfileRepository
from app.services.profile import require_published_profile


class EducationService:
    def __init__(self, session: Session) -> None:
        self.profiles = ProfileRepository(session)
        self.education = EducationRepository(session)

    def list_for_published_profile(self, profile_id: uuid.UUID) -> list[Education]:
        require_published_profile(self.profiles, profile_id=profile_id)
        return self.education.list_for_profile(profile_id)
