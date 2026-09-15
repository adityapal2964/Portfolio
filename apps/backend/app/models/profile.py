from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import CheckConstraint, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text

from app.db.base import Base
from app.models.enums import ContentStatus, sql_in_clause
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.achievement import Achievement
    from app.models.certification import Certification
    from app.models.education import Education
    from app.models.experience import Experience
    from app.models.profile_link import ProfileLink
    from app.models.project import Project


class Profile(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "profiles"
    __table_args__ = (
        CheckConstraint(
            f"status IN ({sql_in_clause(ContentStatus)})",
            name="ck_profiles_status",
        ),
        CheckConstraint("char_length(trim(slug)) > 0", name="ck_profiles_slug_not_empty"),
        CheckConstraint("char_length(trim(display_name)) > 0", name="ck_profiles_display_name_not_empty"),
    )

    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    headline: Mapped[str | None] = mapped_column(String(255))
    location: Mapped[str | None] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(320))
    avatar_url: Mapped[str | None] = mapped_column(String(2048))
    bio_short: Mapped[str | None] = mapped_column(Text)
    bio: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default=ContentStatus.DRAFT.value,
        server_default=ContentStatus.DRAFT.value,
    )
    metadata_payload: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb"),
    )

    projects: Mapped[list[Project]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    experiences: Mapped[list[Experience]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    education_entries: Mapped[list[Education]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    certifications: Mapped[list[Certification]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    achievements: Mapped[list[Achievement]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    links: Mapped[list[ProfileLink]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
