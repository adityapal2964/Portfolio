from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import MediaKind, sql_in_clause
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.project import Project


class ProjectMedia(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "project_media"
    __table_args__ = (
        CheckConstraint(
            f"kind IN ({sql_in_clause(MediaKind)})",
            name="ck_project_media_kind",
        ),
        CheckConstraint("char_length(trim(url)) > 0", name="ck_project_media_url_not_empty"),
        CheckConstraint("sort_order >= 0", name="ck_project_media_sort_order_non_negative"),
        Index("ix_project_media_project_id_sort_order", "project_id", "sort_order"),
        Index(
            "uq_project_media_one_primary",
            "project_id",
            unique=True,
            postgresql_where=text("is_primary = true"),
        ),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    alt_text: Mapped[str | None] = mapped_column(String(255))
    caption: Mapped[str | None] = mapped_column(Text)
    mime_type: Mapped[str | None] = mapped_column(String(127))
    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false"),
    )
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    metadata_payload: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb"),
    )

    project: Mapped[Project] = relationship(back_populates="media")
