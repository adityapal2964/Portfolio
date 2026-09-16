import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.enums import ContentStatus
from app.models.project import Project
from app.repositories.profile import ProfileRepository
from app.repositories.project import ProjectRepository
from app.services.profile import PUBLISHED, require_published_profile


class ProjectService:
    def __init__(self, session: Session) -> None:
        self.profiles = ProfileRepository(session)
        self.projects = ProjectRepository(session)

    def get_published_by_id(self, project_id: uuid.UUID) -> Project:
        project = self.projects.get_by_id(project_id)
        if project is None or project.status != PUBLISHED:
            raise NotFoundError("Project not found")
        require_published_profile(self.profiles, profile_id=project.profile_id)
        return project

    def get_published_by_profile_slug(self, profile_id: uuid.UUID, slug: str) -> Project:
        require_published_profile(self.profiles, profile_id=profile_id)
        project = self.projects.get_by_profile_id_and_slug(profile_id, slug)
        if project is None or project.status != PUBLISHED:
            raise NotFoundError("Project not found")
        return project

    def list_published(
        self,
        *,
        profile_id: uuid.UUID | None = None,
        is_featured: bool | None = None,
        skill: str | None = None,
        category: str | None = None,
        tag: str | None = None,
    ) -> list[Project]:
        if profile_id is not None:
            require_published_profile(self.profiles, profile_id=profile_id)
        return self.projects.list(
            profile_id=profile_id,
            status=ContentStatus.PUBLISHED.value,
            profile_status=PUBLISHED,
            is_featured=is_featured,
            skill_slug=skill,
            category_slug=category,
            tag_slug=tag,
        )

    def list_published_featured(
        self,
        *,
        profile_id: uuid.UUID | None = None,
    ) -> list[Project]:
        return self.list_published(profile_id=profile_id, is_featured=True)
