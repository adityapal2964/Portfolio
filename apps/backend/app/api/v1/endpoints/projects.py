import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.project import ProjectResponse
from app.services.project import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectResponse])
def list_published_projects(
    profile_id: uuid.UUID | None = Query(default=None),
    is_featured: bool | None = Query(default=None),
    skill: str | None = Query(default=None),
    category: str | None = Query(default=None),
    tag: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[ProjectResponse]:
    projects = ProjectService(db).list_published(
        profile_id=profile_id,
        is_featured=is_featured,
        skill=skill,
        category=category,
        tag=tag,
    )
    return [ProjectResponse.model_validate(project) for project in projects]


@router.get("/{project_id}", response_model=ProjectResponse)
def get_published_project(
    project_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> ProjectResponse:
    project = ProjectService(db).get_published_by_id(project_id)
    return ProjectResponse.model_validate(project)
