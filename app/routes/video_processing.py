"""
Video processing endpoints for text extraction
"""

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.models.schemas import TextExtractionResponse, VideoProcessingRequest
from app.services.video_service import text_extractor_from_video, validate_video_file
from app.services.LLM_service import test_api_connection
import requests  # CORRECT!
import cv2
import os
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

router = APIRouter()


@router.post("/extract-text")
async def extract_text_from_video_endpoint(video_file: UploadFile = File(...)):
    try:
        result = await text_extractor_from_video(video_file)
        return {"extracted_text": result["extracted_text"], "frame_count": result.get("frame_count"), "processing_time": result.get("processing_time")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")


@router.post("/test-connection")
def test_connection():
    if test_api_connection():
        print("\nAPI connection successful!")
        import google.generativeai as genai
        print(genai.__version__)
    else:
        raise HTTPException(status_code=500, detail="Failed to connect to the API. Check your API key and network connection.")