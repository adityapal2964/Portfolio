import uuid

from sqlalchemy.orm import Session

from app.models.certification import Certification
from app.repositories.certification import CertificationRepository
from app.repositories.profile import ProfileRepository
from app.services.profile import require_published_profile


class CertificationService:
    def __init__(self, session: Session) -> None:
        self.profiles = ProfileRepository(session)
        self.certifications = CertificationRepository(session)

    def list_for_published_profile(self, profile_id: uuid.UUID) -> list[Certification]:
        require_published_profile(self.profiles, profile_id=profile_id)
        return self.certifications.list_for_profile(profile_id)
