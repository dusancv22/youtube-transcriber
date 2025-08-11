"""
Data models for transcript functionality
"""

from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from datetime import datetime

class TranscriptRequest(BaseModel):
    """Request model for transcript extraction"""
    url: str = Field(..., description="YouTube video URL")
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            }
        }

class ChapterData(BaseModel):
    """Model for video chapter information"""
    title: str = Field(..., description="Chapter title")
    start_time: int = Field(..., description="Start time in seconds")
    end_time: Optional[int] = Field(None, description="End time in seconds")
    timestamp: str = Field(..., description="Human-readable timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Introduction",
                "start_time": 0,
                "end_time": 120,
                "timestamp": "00:00"
            }
        }

class TranscriptResponse(BaseModel):
    """Response model for transcript data"""
    video_id: str = Field(..., description="YouTube video ID")
    title: str = Field(..., description="Video title")
    transcript: str = Field(..., description="Full video transcript")
    chapters: List[ChapterData] = Field(default=[], description="Video chapters")
    duration: int = Field(0, description="Video duration in seconds")
    extracted_at: datetime = Field(default_factory=datetime.now, description="Extraction timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "video_id": "dQw4w9WgXcQ",
                "title": "Never Gonna Give You Up",
                "transcript": "We're no strangers to love...",
                "chapters": [
                    {
                        "title": "Verse 1",
                        "start_time": 0,
                        "end_time": 30,
                        "timestamp": "00:00"
                    }
                ],
                "duration": 212,
                "extracted_at": "2023-12-01T12:00:00"
            }
        }

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")