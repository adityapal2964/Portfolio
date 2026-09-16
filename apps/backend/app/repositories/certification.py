import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.certification import Certification


class CertificationRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, certification_id: uuid.UUID) -> Certification | None:
        return self.session.get(Certification, certification_id)

    def list_for_profile(self, profile_id: uuid.UUID) -> list[Certification]:
        stmt = (
            select(Certification)
            .where(Certification.profile_id == profile_id)
            .order_by(Certification.sort_order, Certification.created_at)
        )
        return list(self.session.scalars(stmt).all())

    def add(self, certification: Certification) -> Certification:
        self.session.add(certification)
        return certification

    def delete(self, certification: Certification) -> None:
        self.session.delete(certification)
