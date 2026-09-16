from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.tag import TagResponse
from app.services.tag import TagService

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("", response_model=list[TagResponse])
def list_tags(db: Session = Depends(get_db)) -> list[TagResponse]:
    return [TagResponse.model_validate(tag) for tag in TagService(db).list()]


@router.get("/{slug}", response_model=TagResponse)
def get_tag(slug: str, db: Session = Depends(get_db)) -> TagResponse:
    return TagResponse.model_validate(TagService(db).get_by_slug(slug))
