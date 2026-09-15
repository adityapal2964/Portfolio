from __future__ import annotations

import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.experience import Experience
from app.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin
from app.models.skill import Skill


class ExperienceSkill(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "experience_skills"
    __table_args__ = (
        UniqueConstraint("experience_id", "skill_id", name="uq_experience_skills_experience_id_skill_id"),
        CheckConstraint("sort_order >= 0", name="ck_experience_skills_sort_order_non_negative"),
        Index("ix_experience_skills_experience_id_sort_order", "experience_id", "sort_order"),
    )

    experience_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("experiences.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("skills.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")

    experience: Mapped[Experience] = relationship(back_populates="skills")
    skill: Mapped[Skill] = relationship(back_populates="experience_skills")
