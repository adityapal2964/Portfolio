import uuid

from sqlalchemy import Select, exists, select
from sqlalchemy.orm import Session, selectinload

from app.models.category import Category
from app.models.project import Project
from app.models.project_category import ProjectCategory
from app.models.project_skill import ProjectSkill
from app.models.project_tag import ProjectTag
from app.models.skill import Skill
from app.models.tag import Tag


class ProjectRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, project_id: uuid.UUID) -> Project | None:
        stmt = self._base_select().where(Project.id == project_id)
        return self.session.scalars(stmt).first()

    def list(
        self,
        *,
        profile_id: uuid.UUID | None = None,
        status: str | None = None,
        is_featured: bool | None = None,
        skill_slug: str | None = None,
        category_slug: str | None = None,
        tag_slug: str | None = None,
    ) -> list[Project]:
        stmt = self._base_select()
        if profile_id is not None:
            stmt = stmt.where(Project.profile_id == profile_id)
        if status is not None:
            stmt = stmt.where(Project.status == status)
        if is_featured is not None:
            stmt = stmt.where(Project.is_featured == is_featured)
        if skill_slug is not None:
            stmt = stmt.where(
                exists(
                    select(1)
                    .select_from(ProjectSkill)
                    .join(Skill, Skill.id == ProjectSkill.skill_id)
                    .where(
                        ProjectSkill.project_id == Project.id,
                        Skill.slug == skill_slug,
                    )
                )
            )
        if category_slug is not None:
            stmt = stmt.where(
                exists(
                    select(1)
                    .select_from(ProjectCategory)
                    .join(Category, Category.id == ProjectCategory.category_id)
                    .where(
                        ProjectCategory.project_id == Project.id,
                        Category.slug == category_slug,
                    )
                )
            )
        if tag_slug is not None:
            stmt = stmt.where(
                exists(
                    select(1)
                    .select_from(ProjectTag)
                    .join(Tag, Tag.id == ProjectTag.tag_id)
                    .where(
                        ProjectTag.project_id == Project.id,
                        Tag.slug == tag_slug,
                    )
                )
            )
        stmt = stmt.order_by(Project.sort_order, Project.created_at)
        return list(self.session.scalars(stmt).unique().all())

    def add(self, project: Project) -> Project:
        self.session.add(project)
        return project

    def delete(self, project: Project) -> None:
        self.session.delete(project)

    def _base_select(self) -> Select[tuple[Project]]:
        return select(Project).options(
            selectinload(Project.links),
            selectinload(Project.media),
            selectinload(Project.skills).selectinload(ProjectSkill.skill),
            selectinload(Project.categories).selectinload(ProjectCategory.category),
            selectinload(Project.tags).selectinload(ProjectTag.tag),
        )
