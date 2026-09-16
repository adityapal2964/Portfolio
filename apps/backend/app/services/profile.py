import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.enums import ContentStatus
from app.models.profile import Profile
from app.repositories.profile import ProfileRepository

PUBLISHED = ContentStatus.PUBLISHED.value


def require_published_profile(
    profiles: ProfileRepository,
    *,
    profile_id: uuid.UUID | None = None,
    slug: str | None = None,
) -> Profile:
    if profile_id is not None:
        profile = profiles.get_by_id(profile_id)
    elif slug is not None:
        profile = profiles.get_by_slug(slug)
    else:
        raise ValueError("profile_id or slug is required")
    if profile is None or profile.status != PUBLISHED:
        raise NotFoundError("Profile not found")
    return profile


class ProfileService:
    def __init__(self, session: Session) -> None:
        self.profiles = ProfileRepository(session)

    def get_published_by_id(self, profile_id: uuid.UUID) -> Profile:
        return require_published_profile(self.profiles, profile_id=profile_id)

    def get_published_by_slug(self, slug: str) -> Profile:
        return require_published_profile(self.profiles, slug=slug)
