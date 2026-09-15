from __future__ import annotations

import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import ProjectLinkKind, sql_in_clause
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.project import Project


class ProjectLink(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "project_links"
    __table_args__ = (
        UniqueConstraint("project_id", "url", name="uq_project_links_project_id_url"),
        CheckConstraint(
            f"kind IN ({sql_in_clause(ProjectLinkKind)})",
            name="ck_project_links_kind",
        ),
        CheckConstraint("char_length(trim(url)) > 0", name="ck_project_links_url_not_empty"),
        CheckConstraint("sort_order >= 0", name="ck_project_links_sort_order_non_negative"),
        Index("ix_project_links_project_id_sort_order", "project_id", "sort_order"),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    label: Mapped[str | None] = mapped_column(String(255))
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")

    project: Mapped[Project] = relationship(back_populates="links")
