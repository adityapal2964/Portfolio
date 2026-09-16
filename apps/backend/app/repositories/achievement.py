import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.achievement import Achievement


class AchievementRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, achievement_id: uuid.UUID) -> Achievement | None:
        return self.session.get(Achievement, achievement_id)

    def list_for_profile(self, profile_id: uuid.UUID) -> list[Achievement]:
        stmt = (
            select(Achievement)
            .where(Achievement.profile_id == profile_id)
            .order_by(Achievement.sort_order, Achievement.created_at)
        )
        return list(self.session.scalars(stmt).all())

    def add(self, achievement: Achievement) -> Achievement:
        self.session.add(achievement)
        return achievement

    def delete(self, achievement: Achievement) -> None:
        self.session.delete(achievement)
