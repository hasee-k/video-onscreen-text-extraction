#!/usr/bin/env python3
"""
Demo script showing how to use the Video Text Extraction API
"""

import json

def demo_api_usage():
    """
    Demonstrate API usage examples
    Note: This is a demonstration script - actual usage requires running the API server
    """
    
    print("🎬 Video On-Screen Text Extraction API Demo")
    print("=" * 50)
    
    print("\n1. Health Check Examples:")
    print("-" * 25)
    
    # Health check example
    health_example = {
        "method": "GET",
        "url": "http://localhost:8000/api/v1/health",
        "expected_response": {
            "status": "healthy",
            "message": "API is running"
        }
    }
    
    print(f"Request: {health_example['method']} {health_example['url']}")
    print(f"Response: {json.dumps(health_example['expected_response'], indent=2)}")
    
    print("\n2. Detailed Health Check:")
    print("-" * 25)
    
    detailed_health_example = {
        "method": "GET", 
        "url": "http://localhost:8000/api/v1/health/detailed",
        "expected_response": {
            "status": "healthy",
            "message": "All systems operational. OpenCV: 4.8.1, Tesseract: 5.x.x"
        }
    }
    
    print(f"Request: {detailed_health_example['method']} {detailed_health_example['url']}")
    print(f"Response: {json.dumps(detailed_health_example['expected_response'], indent=2)}")
    
    print("\n3. Video Text Extraction Example:")
    print("-" * 35)
    
    extraction_example = {
        "method": "POST",
        "url": "http://localhost:8000/api/v1/extract-text",
        "form_data": {
            "video_file": "<video_file_upload>",
            "frame_interval": 30,
            "confidence_threshold": 0.5
        },
        "expected_response": {
            "success": True,
            "message": "Successfully extracted text from 15 frames", 
            "extracted_text": [
                "Welcome to the presentation",
                "Chapter 1: Introduction",
                "Key Points:",
                "- Point one",
                "- Point two"
            ],
            "frame_count": 15,
            "processing_time": 12.34
        }
    }
    
    print(f"Request: {extraction_example['method']} {extraction_example['url']}")
    print("Form Data:")
    for key, value in extraction_example['form_data'].items():
        print(f"  {key}: {value}")
    print(f"Response: {json.dumps(extraction_example['expected_response'], indent=2)}")
    
    print("\n4. Supported Formats Example:")
    print("-" * 30)
    
    formats_example = {
        "method": "GET",
        "url": "http://localhost:8000/api/v1/supported-formats",
        "expected_response": {
            "supported_formats": [".mp4", ".avi", ".mov", ".mkv", ".wmv"],
            "max_file_size": "100MB"
        }
    }
    
    print(f"Request: {formats_example['method']} {formats_example['url']}")
    print(f"Response: {json.dumps(formats_example['expected_response'], indent=2)}")
    
    print("\n5. Python Client Example:")
    print("-" * 25)
    
    client_code = '''
import requests

# Start the API server first:
# uvicorn main:app --reload

# Health check
response = requests.get("http://localhost:8000/api/v1/health")
print("Health:", response.json())

# Extract text from video
with open("sample_video.mp4", "rb") as video_file:
    response = requests.post(
        "http://localhost:8000/api/v1/extract-text",
        files={"video_file": video_file},
        data={
            "frame_interval": 30,
            "confidence_threshold": 0.5
        }
    )
    
result = response.json()
if result["success"]:
    print("Extracted Text:")
    for text in result["extracted_text"]:
        print(f"  - {text}")
else:
    print("Error:", result["message"])
'''
    
    print(client_code)
    
    print("\n📝 Notes:")
    print("-" * 10)
    print("• Install dependencies: pip install -r requirements.txt")
    print("• Start server: uvicorn main:app --reload")
    print("• API will be available at: http://localhost:8000")
    print("• Interactive docs at: http://localhost:8000/docs")
    print("• Alternative docs at: http://localhost:8000/redoc")

if __name__ == "__main__":
    demo_api_usage()