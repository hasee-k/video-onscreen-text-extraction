
import cv2
import pytesseract
import cv2
from PIL import Image, ImageOps, ImageFilter
import json
import numpy as np
import tempfile
import os
import time
from typing import List
from fastapi import UploadFile
from app.models.schemas import TextExtractionResponse, VideoProcessingRequest
from app.services.LLM_service import extract_screen_description


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




def select_frame(image, prev_image):
    # Convert to grayscale
    img1 = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    img2 = cv2.cvtColor(prev_image, cv2.COLOR_RGB2GRAY)

    # Compute grayscale image difference
    grayscale_diff = cv2.absdiff(img1, img2)

    # Compute mean and standard deviation
    mean_diff = np.mean(grayscale_diff)
    std_diff = np.std(grayscale_diff)

    return mean_diff, std_diff

def process_each_frame(frame,prev_frame,frame_count,fps,list_of_texts):
    mean_diff, std_diff = select_frame(frame, prev_frame)

    # Calculate timestamp
    timestamp = frame_count / fps
    timestamp_str = time.strftime('%H:%M:%S', time.gmtime(timestamp))
    timestamp_str_ = timestamp_str.replace(":", "-")

    if std_diff > 4:
        filename = os.path.join("std_diff_frames", f"frame_{frame_count}_at_{timestamp_str_}.jpg")
       # cv2.imwrite(filename, frame)
        extracted_text = text_extractor(frame)
        image_description = extract_screen_description(frame)
        list_of_texts.append({"time_stamp": timestamp_str, "text": extracted_text , "image_description": image_description})

        # if optical_flow_mean_mag(prev_frame, frame) < 10:
        #     filename = os.path.join("std_diff_frames_optical", f"frame_{frame_count}_at_{timestamp_str_}.jpg")
        #     cv2.imwrite(filename, frame)





def text_extractor(image):
    os.makedirs('extracted_frames', exist_ok=True)
    os.makedirs('threshold', exist_ok=True)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(f"extracted_frames/frame_{int(time.time())}.jpg", gray)

    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite(f"threshold/thresh_{int(time.time())}.jpg", thresh)

    extracted_text = pytesseract.image_to_string(gray)

    return extracted_text


def optical_flow_mean_mag(previous, next):
    # Ensure both frames are grayscale
    previous_grey = cv2.cvtColor(previous, cv2.COLOR_BGR2GRAY) if len(previous.shape) == 3 else previous
    next_gray = cv2.cvtColor(next, cv2.COLOR_BGR2GRAY) if len(next.shape) == 3 else next



    flow = cv2.calcOpticalFlowFarneback(previous_grey, next_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    mean_mag = np.mean(mag)
    return mean_mag


async def text_extractor_from_video(video_file: UploadFile):
    print(f"Processing video: {video_file.filename}")

    # Create a temporary file to save the uploaded video
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        try:
            # Read the uploaded file content
            content = await video_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        except Exception as e:
            raise Exception(f"Error saving uploaded file: {str(e)}")

    try:
        # Now use the temporary file path with OpenCV
        cap = cv2.VideoCapture(temp_file_path)

        # Check if video opened successfully
        if not cap.isOpened():
            raise Exception("Error: Could not open video file")

        fps = cap.get(cv2.CAP_PROP_FPS)  # Frames per second of the video
        frame_count = 0
        prev_frame = None
        list_of_texts = []

        # # Paths for saving frames
        # ##mean_diff_folder = "mean_diff_frames"
        # #std_diff_folder = "std_diff_frames"
        # std_diff_folder_optical = "std_diff_frames_optical"
        #
        # # Create folders if they don't exist
        # os.makedirs(mean_diff_folder, exist_ok=True)
        # os.makedirs(std_diff_folder, exist_ok=True)
        # os.makedirs(std_diff_folder_optical, exist_ok=True)

        while True:


            # Read a frame from the video
            hasFrame, image = cap.read()

            # Break the loop if there are no frames left
            if not hasFrame:
                print("End of video reached or cannot fetch the frame.")
                break

            if prev_frame is not None:  # Ensure prev_frame is valid
                process_each_frame(image, prev_frame, frame_count, fps, list_of_texts)

            prev_frame = image.copy()
            frame_count += 1

        # Clean up
        cap.release()
        cv2.destroyAllWindows()
        del cap

        print(f"Extracted text from {len(list_of_texts)} frames.")
        return list_of_texts

    finally:
        # Clean up the temporary file
        try:
            os.unlink(temp_file_path)
        except Exception as e:
            print(f"Warning: Could not delete temporary file {temp_file_path}: {str(e)}")