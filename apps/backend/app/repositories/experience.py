import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.experience import Experience
from app.models.experience_skill import ExperienceSkill


class ExperienceRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, experience_id: uuid.UUID) -> Experience | None:
        stmt = (
            select(Experience)
            .options(selectinload(Experience.skills).selectinload(ExperienceSkill.skill))
            .where(Experience.id == experience_id)
        )
        return self.session.scalars(stmt).first()

    def list_for_profile(self, profile_id: uuid.UUID) -> list[Experience]:
        stmt = (
            select(Experience)
            .options(selectinload(Experience.skills).selectinload(ExperienceSkill.skill))
            .where(Experience.profile_id == profile_id)
            .order_by(Experience.sort_order, Experience.created_at)
        )
        return list(self.session.scalars(stmt).all())

    def add(self, experience: Experience) -> Experience:
        self.session.add(experience)
        return experience

    def delete(self, experience: Experience) -> None:
        self.session.delete(experience)
