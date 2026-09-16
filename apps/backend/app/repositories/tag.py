import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tag import Tag


class TagRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, tag_id: uuid.UUID) -> Tag | None:
        return self.session.get(Tag, tag_id)

    def get_by_slug(self, slug: str) -> Tag | None:
        stmt = select(Tag).where(Tag.slug == slug)
        return self.session.scalars(stmt).first()

    def list(self) -> list[Tag]:
        stmt = select(Tag).order_by(Tag.name)
        return list(self.session.scalars(stmt).all())

    def add(self, tag: Tag) -> Tag:
        self.session.add(tag)
        return tag

    def delete(self, tag: Tag) -> None:
        self.session.delete(tag)
