from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, Index, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.profile import Profile


class Certification(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "certifications"
    __table_args__ = (
        CheckConstraint("char_length(trim(name)) > 0", name="ck_certifications_name_not_empty"),
        CheckConstraint("char_length(trim(issuer)) > 0", name="ck_certifications_issuer_not_empty"),
        CheckConstraint("sort_order >= 0", name="ck_certifications_sort_order_non_negative"),
        CheckConstraint(
            "expires_on IS NULL OR issued_on IS NULL OR expires_on >= issued_on",
            name="ck_certifications_date_range",
        ),
        Index("ix_certifications_profile_id_sort_order", "profile_id", "sort_order"),
        Index(
            "uq_certifications_profile_id_credential_id",
            "profile_id",
            "credential_id",
            unique=True,
            postgresql_where=text("credential_id IS NOT NULL"),
        ),
    )

    profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    issuer: Mapped[str] = mapped_column(String(255), nullable=False)
    issued_on: Mapped[date | None] = mapped_column(Date)
    expires_on: Mapped[date | None] = mapped_column(Date)
    credential_id: Mapped[str | None] = mapped_column(String(255))
    credential_url: Mapped[str | None] = mapped_column(String(2048))
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")

    profile: Mapped[Profile] = relationship(back_populates="certifications")
