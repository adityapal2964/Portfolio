import uuid

from sqlalchemy.orm import Session

from app.models.achievement import Achievement
from app.repositories.achievement import AchievementRepository
from app.repositories.profile import ProfileRepository
from app.services.profile import require_published_profile


class AchievementService:
    def __init__(self, session: Session) -> None:
        self.profiles = ProfileRepository(session)
        self.achievements = AchievementRepository(session)

    def list_for_published_profile(self, profile_id: uuid.UUID) -> list[Achievement]:
        require_published_profile(self.profiles, profile_id=profile_id)
        return self.achievements.list_for_profile(profile_id)
