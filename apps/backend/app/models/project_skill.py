from __future__ import annotations

import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin
from app.models.project import Project
from app.models.skill import Skill


class ProjectSkill(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "project_skills"
    __table_args__ = (
        UniqueConstraint("project_id", "skill_id", name="uq_project_skills_project_id_skill_id"),
        CheckConstraint("sort_order >= 0", name="ck_project_skills_sort_order_non_negative"),
        Index("ix_project_skills_project_id_sort_order", "project_id", "sort_order"),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("skills.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")

    project: Mapped[Project] = relationship(back_populates="skills")
    skill: Mapped[Skill] = relationship(back_populates="project_skills")
