from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import ContentStatus, sql_in_clause
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.profile import Profile
    from app.models.project_category import ProjectCategory
    from app.models.project_link import ProjectLink
    from app.models.project_media import ProjectMedia
    from app.models.project_skill import ProjectSkill
    from app.models.project_tag import ProjectTag


class Project(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "projects"
    __table_args__ = (
        UniqueConstraint("profile_id", "slug", name="uq_projects_profile_id_slug"),
        CheckConstraint(
            f"status IN ({sql_in_clause(ContentStatus)})",
            name="ck_projects_status",
        ),
        CheckConstraint("char_length(trim(slug)) > 0", name="ck_projects_slug_not_empty"),
        CheckConstraint("char_length(trim(title)) > 0", name="ck_projects_title_not_empty"),
        CheckConstraint("sort_order >= 0", name="ck_projects_sort_order_non_negative"),
        CheckConstraint(
            "ended_on IS NULL OR started_on IS NULL OR ended_on >= started_on",
            name="ck_projects_date_range",
        ),
        Index("ix_projects_profile_id_sort_order", "profile_id", "sort_order"),
        Index("ix_projects_profile_id_status", "profile_id", "status"),
        Index(
            "ix_projects_profile_id_sort_order_featured",
            "profile_id",
            "sort_order",
            postgresql_where=text("is_featured = true"),
        ),
    )

    profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    body: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default=ContentStatus.DRAFT.value,
        server_default=ContentStatus.DRAFT.value,
    )
    is_featured: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false"),
    )
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    started_on: Mapped[date | None] = mapped_column(Date)
    ended_on: Mapped[date | None] = mapped_column(Date)
    metadata_payload: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb"),
    )

    profile: Mapped[Profile] = relationship(back_populates="projects")
    categories: Mapped[list[ProjectCategory]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    tags: Mapped[list[ProjectTag]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    skills: Mapped[list[ProjectSkill]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    links: Mapped[list[ProjectLink]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    media: Mapped[list[ProjectMedia]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
