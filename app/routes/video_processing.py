"""
Video processing endpoints for text extraction
"""

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.models.schemas import TextExtractionResponse, VideoProcessingRequest
from app.services.video_service import text_extractor_from_video, validate_video_file

router = APIRouter()


@router.post("/extract-text")
async def extract_text_from_video_endpoint(video_file: UploadFile = File(...)):
    try:
        result = await text_extractor_from_video(video_file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")

