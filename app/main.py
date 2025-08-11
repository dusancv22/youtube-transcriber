"""
YouTube Transcriber FastAPI Application
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from pathlib import Path

from .models.transcript import TranscriptRequest, TranscriptResponse
from .services.transcript_service import TranscriptService
from .services.chapter_service import ChapterService
from .services.url_extractor import URLExtractor

# Initialize FastAPI app
app = FastAPI(
    title="YouTube Transcriber",
    description="A web application for transcribing YouTube videos",
    version="1.0.0"
)

# Get the directory of the current file
BASE_DIR = Path(__file__).resolve().parent

# Mount static files
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Initialize services
transcript_service = TranscriptService()
chapter_service = ChapterService()
url_extractor = URLExtractor()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main application page"""
    try:
        with open(BASE_DIR / "static" / "index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Frontend not found")

@app.post("/api/transcript", response_model=TranscriptResponse)
async def get_transcript(request: TranscriptRequest):
    """Get transcript for a YouTube video"""
    try:
        # Extract video ID from URL
        video_id = url_extractor.extract_video_id(request.url)
        
        if not video_id:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")
        
        # Get transcript
        transcript_data = await transcript_service.get_transcript(video_id)
        
        # Get chapters if available
        chapters = await chapter_service.get_chapters(video_id)
        
        return TranscriptResponse(
            video_id=video_id,
            title=transcript_data.get("title", ""),
            transcript=transcript_data.get("transcript", ""),
            chapters=chapters,
            duration=transcript_data.get("duration", 0)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "YouTube Transcriber"}

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Handle 404 errors"""
    return HTMLResponse(
        content="<h1>404 - Page Not Found</h1>",
        status_code=404
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    """Handle 500 errors"""
    return HTMLResponse(
        content="<h1>500 - Internal Server Error</h1>",
        status_code=500
    )