from fastapi import APIRouter

from app.api.v1.endpoints import health, profiles, projects

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(profiles.router)
api_router.include_router(projects.router)
