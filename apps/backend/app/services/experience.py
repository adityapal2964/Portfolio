import uuid

from sqlalchemy.orm import Session

from app.models.experience import Experience
from app.repositories.experience import ExperienceRepository
from app.repositories.profile import ProfileRepository
from app.services.profile import require_published_profile


class ExperienceService:
    def __init__(self, session: Session) -> None:
        self.profiles = ProfileRepository(session)
        self.experiences = ExperienceRepository(session)

    def list_for_published_profile(self, profile_id: uuid.UUID) -> list[Experience]:
        require_published_profile(self.profiles, profile_id=profile_id)
        return self.experiences.list_for_profile(profile_id)
