from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.project_category import ProjectCategory


class Category(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "categories"
    __table_args__ = (
        CheckConstraint("char_length(trim(slug)) > 0", name="ck_categories_slug_not_empty"),
        CheckConstraint("char_length(trim(name)) > 0", name="ck_categories_name_not_empty"),
        CheckConstraint("sort_order >= 0", name="ck_categories_sort_order_non_negative"),
    )

    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")

    project_categories: Mapped[list[ProjectCategory]] = relationship(back_populates="category")
