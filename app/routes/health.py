"""
Health check endpoints
"""

from fastapi import APIRouter
from app.models.schemas import HealthResponse
from app.services.health_service import check_system_health

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify API status
    """
    return await check_system_health()


@router.get("/health/detailed", response_model=HealthResponse)
async def detailed_health_check():
    """
    Detailed health check including dependencies
    """
    return await check_system_health(detailed=True)