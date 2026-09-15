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
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.experience_skill import ExperienceSkill
    from app.models.profile import Profile


class Experience(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "experiences"
    __table_args__ = (
        CheckConstraint(
            "(is_current = false) OR (end_date IS NULL)",
            name="ck_experiences_current_end_date",
        ),
        CheckConstraint(
            "end_date IS NULL OR start_date IS NULL OR end_date >= start_date",
            name="ck_experiences_date_range",
        ),
        CheckConstraint("char_length(trim(company_name)) > 0", name="ck_experiences_company_name_not_empty"),
        CheckConstraint("char_length(trim(title)) > 0", name="ck_experiences_title_not_empty"),
        CheckConstraint("sort_order >= 0", name="ck_experiences_sort_order_non_negative"),
        Index("ix_experiences_profile_id_sort_order", "profile_id", "sort_order"),
    )

    profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    company_url: Mapped[str | None] = mapped_column(String(2048))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str | None] = mapped_column(String(255))
    employment_type: Mapped[str | None] = mapped_column(String(64))
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    is_current: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false"),
    )
    summary: Mapped[str | None] = mapped_column(Text)
    body: Mapped[str | None] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    metadata_payload: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb"),
    )

    profile: Mapped[Profile] = relationship(back_populates="experiences")
    skills: Mapped[list[ExperienceSkill]] = relationship(
        back_populates="experience",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
