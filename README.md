# Video On-Screen Text Extraction API

A FastAPI-based web service for extracting text from video files using Optical Character Recognition (OCR).

## Project Structure

This project follows FastAPI best practices with proper separation of concerns:

```
├── main.py                     # Application entry point
├── requirements.txt            # Project dependencies  
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic models for validation
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── health.py           # Health check endpoints
│   │   └── video_processing.py # Video processing endpoints
│   └── services/
│       ├── __init__.py
│       ├── health_service.py   # Health check business logic
│       └── video_service.py    # Video processing functions
└── test_structure.py           # Project structure validation
```

## Features

- **Health Check Endpoints**: Monitor API status and dependencies
- **Video Text Extraction**: Extract text from video frames using OCR
- **Configurable Processing**: Adjust frame intervals and confidence thresholds
- **Multiple Video Formats**: Support for MP4, AVI, MOV, MKV, WMV
- **Proper Error Handling**: Comprehensive error responses
- **CORS Support**: Cross-origin resource sharing enabled

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
# Method 1: Direct execution
python main.py

# Method 2: Using uvicorn
uvicorn main:app --reload

# Method 3: Production deployment
uvicorn main:app --host 0.0.0.0 --port 8000
```

### API Endpoints

#### Health Check
- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/detailed` - Detailed health check with dependencies

#### Video Processing  
- `POST /api/v1/extract-text` - Extract text from uploaded video
- `GET /api/v1/supported-formats` - Get supported video formats

### Example Usage

```python
import requests

# Health check
response = requests.get("http://localhost:8000/api/v1/health")
print(response.json())

# Extract text from video
with open("video.mp4", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/v1/extract-text",
        files={"video_file": f},
        data={"frame_interval": 30, "confidence_threshold": 0.5}
    )
print(response.json())
```

## Architecture

### Separation of Concerns

1. **main.py**: FastAPI application setup, middleware, and router registration
2. **app/routes/**: API endpoint definitions and request/response handling
3. **app/services/**: Business logic and core functionality
4. **app/models/**: Pydantic models for data validation

### Dependencies

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for running the application
- **OpenCV**: Computer vision library for video processing
- **Pytesseract**: OCR engine for text extraction
- **Pydantic**: Data validation using Python type hints

## Testing Structure

Run the structure validation test:

```bash
python test_structure.py
```

This validates:
- All required files exist
- Proper separation of concerns
- Correct FastAPI setup
- Business logic organization