from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.skill import SkillResponse
from app.services.skill import SkillService

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("", response_model=list[SkillResponse])
def list_skills(db: Session = Depends(get_db)) -> list[SkillResponse]:
    return [SkillResponse.model_validate(skill) for skill in SkillService(db).list()]


@router.get("/{slug}", response_model=SkillResponse)
def get_skill(slug: str, db: Session = Depends(get_db)) -> SkillResponse:
    return SkillResponse.model_validate(SkillService(db).get_by_slug(slug))
