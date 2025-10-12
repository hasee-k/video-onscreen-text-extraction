from importlib import reload

from fastapi import FastAPI

from app.routes import video_processing

from fastapi.middleware.cors import CORSMiddleware
from frontend_router import router as frontend_router

# Initialize FastAPI application
app = FastAPI(
    title="Video On-Screen Text Extraction API",
    description="API for extracting text from video frames using OCR",
    version="1.0.0"
)

origins = [
    "http://localhost:3000",  # React dev server
    "http://127.0.0.1:3000"
]

allow_origins=["*"],


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers

app.include_router(frontend_router)

app.include_router(video_processing.router, prefix="/api/v1", tags=["video"])
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)