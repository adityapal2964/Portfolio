import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, category_id: uuid.UUID) -> Category | None:
        return self.session.get(Category, category_id)

    def get_by_slug(self, slug: str) -> Category | None:
        stmt = select(Category).where(Category.slug == slug)
        return self.session.scalars(stmt).first()

    def list(self) -> list[Category]:
        stmt = select(Category).order_by(Category.sort_order, Category.name)
        return list(self.session.scalars(stmt).all())

    def add(self, category: Category) -> Category:
        self.session.add(category)
        return category

    def delete(self, category: Category) -> None:
        self.session.delete(category)
