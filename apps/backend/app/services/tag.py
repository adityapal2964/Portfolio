from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.tag import Tag
from app.repositories.tag import TagRepository


class TagService:
    def __init__(self, session: Session) -> None:
        self.tags = TagRepository(session)

    def list(self) -> list[Tag]:
        return self.tags.list()

    def get_by_slug(self, slug: str) -> Tag:
        tag = self.tags.get_by_slug(slug)
        if tag is None:
            raise NotFoundError("Tag not found")
        return tag
