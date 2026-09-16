import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.skill import Skill


class SkillRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, skill_id: uuid.UUID) -> Skill | None:
        return self.session.get(Skill, skill_id)

    def get_by_slug(self, slug: str) -> Skill | None:
        stmt = select(Skill).where(Skill.slug == slug)
        return self.session.scalars(stmt).first()

    def list(self) -> list[Skill]:
        stmt = select(Skill).order_by(Skill.name)
        return list(self.session.scalars(stmt).all())

    def add(self, skill: Skill) -> Skill:
        self.session.add(skill)
        return skill

    def delete(self, skill: Skill) -> None:
        self.session.delete(skill)
