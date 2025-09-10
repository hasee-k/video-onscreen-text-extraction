"""
Pydantic models for API request and response validation
"""

from typing import List, Optional
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    message: str


class TextExtractionResponse(BaseModel):
    """Response model for text extraction results"""
    success: bool
    message: str
    extracted_text: Optional[List[str]] = None
    frame_count: Optional[int] = None
    processing_time: Optional[float] = None


class VideoProcessingRequest(BaseModel):
    """Request model for video processing parameters"""
    frame_interval: Optional[int] = 30  # Extract text every N frames
    confidence_threshold: Optional[float] = 0.5  # OCR confidence threshold