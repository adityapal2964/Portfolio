from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.experience_skill import ExperienceSkill
    from app.models.project_skill import ProjectSkill


class Skill(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "skills"
    __table_args__ = (
        CheckConstraint("char_length(trim(slug)) > 0", name="ck_skills_slug_not_empty"),
        CheckConstraint("char_length(trim(name)) > 0", name="ck_skills_name_not_empty"),
    )

    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    category: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)

    project_skills: Mapped[list[ProjectSkill]] = relationship(back_populates="skill")
    experience_skills: Mapped[list[ExperienceSkill]] = relationship(back_populates="skill")
