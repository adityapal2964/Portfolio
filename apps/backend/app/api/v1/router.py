from fastapi import APIRouter

from app.api.v1.endpoints import categories, health, profiles, projects, skills, tags

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(profiles.router)
api_router.include_router(projects.router)
api_router.include_router(skills.router)
api_router.include_router(categories.router)
api_router.include_router(tags.router)
