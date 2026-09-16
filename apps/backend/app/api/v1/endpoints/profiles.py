from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.profile import ProfileResponse
from app.services.profile import ProfileService

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/{slug}", response_model=ProfileResponse)
def get_published_profile(slug: str, db: Session = Depends(get_db)) -> ProfileResponse:
    profile = ProfileService(db).get_published_by_slug(slug)
    return ProfileResponse.model_validate(profile)
