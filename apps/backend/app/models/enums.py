from enum import StrEnum


class ContentStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class ProjectLinkKind(StrEnum):
    GITHUB = "github"
    LIVE_DEMO = "live_demo"
    DOCS = "docs"
    PACKAGE = "package"
    OTHER = "other"


class ProfileLinkKind(StrEnum):
    GITHUB = "github"
    LINKEDIN = "linkedin"
    X = "x"
    WEBSITE = "website"
    EMAIL = "email"
    OTHER = "other"


class MediaKind(StrEnum):
    IMAGE = "image"
    VIDEO = "video"
    DIAGRAM = "diagram"


def sql_in_clause(values: tuple[str, ...] | type[StrEnum]) -> str:
    items = tuple(values) if isinstance(values, tuple) else tuple(member.value for member in values)
    return ", ".join(f"'{item}'" for item in items)
