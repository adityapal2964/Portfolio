from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin
from app.models.project import Project
from app.models.tag import Tag


class ProjectTag(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "project_tags"
    __table_args__ = (
        UniqueConstraint("project_id", "tag_id", name="uq_project_tags_project_id_tag_id"),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    tag_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tags.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    project: Mapped[Project] = relationship(back_populates="tags")
    tag: Mapped[Tag] = relationship(back_populates="project_tags")
