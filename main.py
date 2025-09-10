"""
Main FastAPI application entry point.
Handles application initialization and routing setup.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, video_processing

# Initialize FastAPI application
app = FastAPI(
    title="Video On-Screen Text Extraction API",
    description="API for extracting text from video frames using OCR",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(video_processing.router, prefix="/api/v1", tags=["video"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)