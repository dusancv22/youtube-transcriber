# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Setup & Installation
```bash
# Create virtual environment (Windows)
python -m venv venv

# Activate virtual environment (Windows)
./venv/Scripts/activate

# Install dependencies
./venv/Scripts/pip install -r requirements.txt
```

### Running the Application
```bash
# Run with auto-reload (development)
./venv/Scripts/python run.py

# Direct uvicorn run
./venv/Scripts/uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Testing Specific Features
```bash
# Test URL extraction directly
./venv/Scripts/python -c "from app.services.url_extractor import URLExtractor; ext = URLExtractor(); print(ext.extract_video_id('YOUR_URL_HERE'))"

# Test transcript extraction
./venv/Scripts/python -c "from youtube_transcript_api import YouTubeTranscriptApi; api = YouTubeTranscriptApi(); print(api.list('VIDEO_ID'))"
```

## Architecture Overview

### Service-Based Backend Structure
The application uses a modular service architecture where each service handles a specific domain:

1. **TranscriptService** (`app/services/transcript_service.py`)
   - Primary service for YouTube transcript extraction
   - Handles language prioritization (English first, then fallbacks)
   - Uses `YouTubeTranscriptApi` instance methods (not class methods)
   - Key method: `_extract_transcript()` - handles multiple fallback strategies

2. **URLExtractor** (`app/services/url_extractor.py`)
   - Extracts video IDs from various YouTube URL formats
   - Supports: `/watch?v=`, `/live/`, `/shorts/`, `/embed/`, `youtu.be/`
   - Uses both regex patterns and URL parsing for robustness
   - Critical for frontend validation alignment

3. **ChapterService** (`app/services/chapter_service.py`)
   - Extracts chapter information from video metadata
   - Parses timestamps from video descriptions
   - Uses `yt-dlp` for metadata extraction

### Frontend-Backend Coordination
The frontend JavaScript (`app/static/js/main.js`) mirrors backend validation:
- URL validation must match between frontend `isValidYouTubeUrl()` and backend `URLExtractor`
- When adding new URL formats, update BOTH locations
- Frontend performs initial validation, backend performs authoritative extraction

### API Flow
1. Frontend validates URL format using regex patterns
2. POST request to `/api/transcript` with YouTube URL
3. Backend extracts video ID using URLExtractor
4. TranscriptService attempts extraction with fallback chain
5. ChapterService enriches with metadata if available
6. Response includes transcript, title, duration, and chapters

## Critical Implementation Details

### YouTube Transcript API Usage
```python
# CORRECT - Use instance methods
api = YouTubeTranscriptApi()
transcript_list = api.list(video_id)

# INCORRECT - Don't use as class methods
YouTubeTranscriptApi.list_transcripts(video_id)  # This will fail
```

### URL Format Support
When adding new URL formats:
1. Update regex in `app/services/url_extractor.py` (line ~17-32)
2. Add parsing logic in `_extract_with_urlparse()` method
3. Update frontend validation in `app/static/js/main.js` `isValidYouTubeUrl()`
4. Test both frontend and backend validation

### Download Filename Generation
The `generateFilename()` function in `main.js` creates user-friendly filenames:
- Format: `[Video Title] - Transcript.txt`
- Handles undefined/null titles gracefully
- Replaces filesystem-unsafe characters with dashes
- Always ensures `.txt` extension

## Known Issues & Solutions

### Live URL Video Unavailable
Live URLs (`/live/VIDEO_ID`) may fail if:
- Video is currently streaming (no transcript yet)
- Video is private or deleted
- Solution: Test with completed live streams that have captions

### Transcript Language Fallback
The service attempts extraction in this order:
1. English manual transcript
2. English auto-generated transcript  
3. First available transcript in any language
4. Failure if no transcripts exist

### Frontend Cache Issues
After JavaScript changes:
- Hard refresh browser (Ctrl+F5)
- Server auto-reloads Python changes
- Static files may be cached by browser

## Project Structure Context

```
YouTube_Transcriber/
├── app/
│   ├── main.py          # FastAPI application entry point
│   ├── models/          # Pydantic models for request/response
│   ├── services/        # Business logic services
│   └── static/          # Frontend assets (HTML, CSS, JS)
├── venv/                # Virtual environment (excluded from git)
├── requirements.txt     # Python dependencies
├── run.py              # Application launcher
├── PLANNING.md         # Project architecture and roadmap
└── TASKS.md           # Task tracking and priorities
```

## Development Workflow

1. Always use virtual environment to avoid dependency conflicts
2. Server runs with auto-reload - changes to Python files reload automatically
3. Frontend changes require browser refresh
4. Test URL extraction separately when debugging URL issues
5. Check server console for detailed error messages
6. Use browser DevTools for frontend debugging

## API Endpoints

- `GET /` - Serves the web interface
- `POST /api/transcript` - Extracts transcript (expects JSON with `url` field)
- `GET /api/health` - Health check endpoint
- `GET /docs` - Auto-generated API documentation (FastAPI feature)