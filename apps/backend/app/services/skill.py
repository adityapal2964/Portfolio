from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.skill import Skill
from app.repositories.skill import SkillRepository


class SkillService:
    def __init__(self, session: Session) -> None:
        self.skills = SkillRepository(session)

    def list(self) -> list[Skill]:
        return self.skills.list()

    def get_by_slug(self, slug: str) -> Skill:
        skill = self.skills.get_by_slug(slug)
        if skill is None:
            raise NotFoundError("Skill not found")
        return skill
