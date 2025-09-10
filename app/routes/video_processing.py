"""
Video processing endpoints for text extraction
"""

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.models.schemas import TextExtractionResponse, VideoProcessingRequest
from app.services.video_service import extract_text_from_video, validate_video_file

router = APIRouter()


@router.post("/extract-text", response_model=TextExtractionResponse)
async def extract_text_from_video_endpoint(
    video_file: UploadFile = File(...),
    params: VideoProcessingRequest = Depends()
):
    """
    Extract text from uploaded video file
    
    - **video_file**: Video file to process (MP4, AVI, MOV supported)
    - **frame_interval**: Extract text every N frames (default: 30)
    - **confidence_threshold**: OCR confidence threshold (default: 0.5)
    """
    # Validate video file
    if not validate_video_file(video_file):
        raise HTTPException(status_code=400, detail="Invalid video file format")
    
    try:
        result = await extract_text_from_video(video_file, params)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")


@router.get("/supported-formats")
async def get_supported_formats():
    """
    Get list of supported video formats
    """
    return {
        "supported_formats": [".mp4", ".avi", ".mov", ".mkv", ".wmv"],
        "max_file_size": "100MB"
    }