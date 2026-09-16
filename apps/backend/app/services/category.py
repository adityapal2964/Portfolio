from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.category import Category
from app.repositories.category import CategoryRepository


class CategoryService:
    def __init__(self, session: Session) -> None:
        self.categories = CategoryRepository(session)

    def list(self) -> list[Category]:
        return self.categories.list()

    def get_by_slug(self, slug: str) -> Category:
        category = self.categories.get_by_slug(slug)
        if category is None:
            raise NotFoundError("Category not found")
        return category
