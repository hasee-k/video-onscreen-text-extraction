from importlib import reload

from fastapi import FastAPI

from app.routes import video_processing

# Initialize FastAPI application
app = FastAPI(
    title="Video On-Screen Text Extraction API",
    description="API for extracting text from video frames using OCR",
    version="1.0.0"
)

# Include routers

app.include_router(video_processing.router, prefix="/api/v1", tags=["video"])
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)