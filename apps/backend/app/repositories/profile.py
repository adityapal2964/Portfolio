import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.profile import Profile


class ProfileRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, profile_id: uuid.UUID) -> Profile | None:
        stmt = (
            select(Profile)
            .options(selectinload(Profile.links))
            .where(Profile.id == profile_id)
        )
        return self.session.scalars(stmt).first()

    def get_by_slug(self, slug: str) -> Profile | None:
        stmt = (
            select(Profile)
            .options(selectinload(Profile.links))
            .where(Profile.slug == slug)
        )
        return self.session.scalars(stmt).first()

    def add(self, profile: Profile) -> Profile:
        self.session.add(profile)
        return profile

    def delete(self, profile: Profile) -> None:
        self.session.delete(profile)
