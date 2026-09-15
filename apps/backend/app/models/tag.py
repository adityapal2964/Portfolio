from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.project_tag import ProjectTag


class Tag(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "tags"
    __table_args__ = (
        CheckConstraint("char_length(trim(slug)) > 0", name="ck_tags_slug_not_empty"),
        CheckConstraint("char_length(trim(name)) > 0", name="ck_tags_name_not_empty"),
    )

    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    project_tags: Mapped[list[ProjectTag]] = relationship(back_populates="tag")
