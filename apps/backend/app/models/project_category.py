from __future__ import annotations

import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.category import Category
from app.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin
from app.models.project import Project


class ProjectCategory(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "project_categories"
    __table_args__ = (
        UniqueConstraint("project_id", "category_id", name="uq_project_categories_project_id_category_id"),
        CheckConstraint("sort_order >= 0", name="ck_project_categories_sort_order_non_negative"),
        Index("ix_project_categories_project_id_sort_order", "project_id", "sort_order"),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")

    project: Mapped[Project] = relationship(back_populates="categories")
    category: Mapped[Category] = relationship(back_populates="project_categories")
