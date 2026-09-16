import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.achievement import AchievementResponse
from app.schemas.certification import CertificationResponse
from app.schemas.education import EducationResponse
from app.schemas.experience import ExperienceResponse
from app.schemas.profile import ProfileResponse
from app.schemas.project import ProjectResponse
from app.services.achievement import AchievementService
from app.services.certification import CertificationService
from app.services.education import EducationService
from app.services.experience import ExperienceService
from app.services.profile import ProfileService
from app.services.project import ProjectService

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/{profile_id}/experience", response_model=list[ExperienceResponse])
def list_published_profile_experience(
    profile_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> list[ExperienceResponse]:
    experiences = ExperienceService(db).list_for_published_profile(profile_id)
    return [ExperienceResponse.model_validate(item) for item in experiences]


@router.get("/{profile_id}/education", response_model=list[EducationResponse])
def list_published_profile_education(
    profile_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> list[EducationResponse]:
    entries = EducationService(db).list_for_published_profile(profile_id)
    return [EducationResponse.model_validate(item) for item in entries]


@router.get("/{profile_id}/certifications", response_model=list[CertificationResponse])
def list_published_profile_certifications(
    profile_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> list[CertificationResponse]:
    certifications = CertificationService(db).list_for_published_profile(profile_id)
    return [CertificationResponse.model_validate(item) for item in certifications]


@router.get("/{profile_id}/achievements", response_model=list[AchievementResponse])
def list_published_profile_achievements(
    profile_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> list[AchievementResponse]:
    achievements = AchievementService(db).list_for_published_profile(profile_id)
    return [AchievementResponse.model_validate(item) for item in achievements]


@router.get("/{profile_id}/projects/{slug}", response_model=ProjectResponse)
def get_published_profile_project(
    profile_id: uuid.UUID,
    slug: str,
    db: Session = Depends(get_db),
) -> ProjectResponse:
    project = ProjectService(db).get_published_by_profile_slug(profile_id, slug)
    return ProjectResponse.model_validate(project)


@router.get("/{profile_id}/projects", response_model=list[ProjectResponse])
def list_published_profile_projects(
    profile_id: uuid.UUID,
    is_featured: bool | None = Query(default=None),
    skill: str | None = Query(default=None, min_length=1),
    category: str | None = Query(default=None, min_length=1),
    tag: str | None = Query(default=None, min_length=1),
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


@router.get("/{slug}", response_model=ProfileResponse)
def get_published_profile(slug: str, db: Session = Depends(get_db)) -> ProfileResponse:
    profile = ProfileService(db).get_published_by_slug(slug)
    return ProfileResponse.model_validate(profile)
