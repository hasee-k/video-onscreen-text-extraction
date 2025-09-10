"""
Video processing service functions
"""

import cv2
import pytesseract
import numpy as np
import tempfile
import os
import time
from typing import List
from fastapi import UploadFile
from app.models.schemas import TextExtractionResponse, VideoProcessingRequest


def validate_video_file(video_file: UploadFile) -> bool:
    """
    Validate uploaded video file
    
    Args:
        video_file: Uploaded video file
        
    Returns:
        bool: True if valid video file
    """
    allowed_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
    file_extension = os.path.splitext(video_file.filename.lower())[1]
    return file_extension in allowed_extensions


async def extract_text_from_video(
    video_file: UploadFile, 
    params: VideoProcessingRequest
) -> TextExtractionResponse:
    """
    Extract text from video frames using OCR
    
    Args:
        video_file: Uploaded video file
        params: Processing parameters
        
    Returns:
        TextExtractionResponse with extracted text
    """
    start_time = time.time()
    extracted_texts = []
    frame_count = 0
    
    # Create temporary file for video processing
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
        temp_file.write(await video_file.read())
        temp_file_path = temp_file.name
    
    try:
        # Open video file
        cap = cv2.VideoCapture(temp_file_path)
        
        if not cap.isOpened():
            return TextExtractionResponse(
                success=False,
                message="Could not open video file"
            )
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        current_frame = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process every nth frame based on frame_interval
            if current_frame % params.frame_interval == 0:
                text = extract_text_from_frame(frame, params.confidence_threshold)
                if text.strip():  # Only add non-empty text
                    extracted_texts.append(text.strip())
                frame_count += 1
            
            current_frame += 1
        
        cap.release()
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        processing_time = time.time() - start_time
        
        return TextExtractionResponse(
            success=True,
            message=f"Successfully extracted text from {frame_count} frames",
            extracted_text=list(set(extracted_texts)),  # Remove duplicates
            frame_count=frame_count,
            processing_time=round(processing_time, 2)
        )
        
    except Exception as e:
        # Clean up temporary file in case of error
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        
        return TextExtractionResponse(
            success=False,
            message=f"Error processing video: {str(e)}"
        )


def extract_text_from_frame(frame: np.ndarray, confidence_threshold: float = 0.5) -> str:
    """
    Extract text from a single video frame
    
    Args:
        frame: Video frame as numpy array
        confidence_threshold: Minimum confidence for OCR results
        
    Returns:
        str: Extracted text from frame
    """
    # Convert frame to grayscale for better OCR performance
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply some preprocessing to improve OCR accuracy
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply threshold to get a binary image
    _, threshold = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Use pytesseract to extract text with confidence scores
    try:
        data = pytesseract.image_to_data(threshold, output_type=pytesseract.Output.DICT)
        
        # Filter text based on confidence threshold
        extracted_text = []
        for i, confidence in enumerate(data['conf']):
            if int(confidence) > confidence_threshold * 100:  # pytesseract confidence is 0-100
                text = data['text'][i].strip()
                if text:
                    extracted_text.append(text)
        
        return ' '.join(extracted_text)
    
    except Exception:
        # Fallback to simple text extraction if confidence filtering fails
        return pytesseract.image_to_string(threshold).strip()