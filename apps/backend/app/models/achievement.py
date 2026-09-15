from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.profile import Profile


class Achievement(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "achievements"
    __table_args__ = (
        CheckConstraint("char_length(trim(title)) > 0", name="ck_achievements_title_not_empty"),
        CheckConstraint("sort_order >= 0", name="ck_achievements_sort_order_non_negative"),
        Index("ix_achievements_profile_id_sort_order", "profile_id", "sort_order"),
    )

    profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str | None] = mapped_column(String(2048))
    occurred_on: Mapped[date | None] = mapped_column(Date)
    summary: Mapped[str | None] = mapped_column(Text)
    body: Mapped[str | None] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")

    profile: Mapped[Profile] = relationship(back_populates="achievements")
