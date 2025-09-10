"""
Health check service functions
"""

import cv2
import pytesseract
from app.models.schemas import HealthResponse


async def check_system_health(detailed: bool = False) -> HealthResponse:
    """
    Check system health and dependencies
    
    Args:
        detailed: Whether to perform detailed dependency checks
        
    Returns:
        HealthResponse with status information
    """
    try:
        if detailed:
            # Check OpenCV
            cv2_version = cv2.__version__
            
            # Check Tesseract
            try:
                tesseract_version = pytesseract.get_tesseract_version()
            except Exception:
                return HealthResponse(
                    status="unhealthy",
                    message="Tesseract OCR not available"
                )
            
            return HealthResponse(
                status="healthy",
                message=f"All systems operational. OpenCV: {cv2_version}, Tesseract: {tesseract_version}"
            )
        else:
            return HealthResponse(
                status="healthy",
                message="API is running"
            )
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            message=f"Health check failed: {str(e)}"
        )