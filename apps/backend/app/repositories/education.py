import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.education import Education


class EducationRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, education_id: uuid.UUID) -> Education | None:
        return self.session.get(Education, education_id)

    def list_for_profile(self, profile_id: uuid.UUID) -> list[Education]:
        stmt = (
            select(Education)
            .where(Education.profile_id == profile_id)
            .order_by(Education.sort_order, Education.created_at)
        )
        return list(self.session.scalars(stmt).all())

    def add(self, education: Education) -> Education:
        self.session.add(education)
        return education

    def delete(self, education: Education) -> None:
        self.session.delete(education)
