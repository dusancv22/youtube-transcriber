# PLANNING.md

## Project Overview

**Name:** YouTube Transcriber  
**Purpose:** A comprehensive web application for extracting YouTube video transcripts with support for multiple URL formats, chapter detection, and various export options  
**Status:** Production-ready  
**Version:** 1.0.0  

The YouTube Transcriber provides a clean, modern interface for users to extract transcripts from YouTube videos. It supports various YouTube URL formats and prioritizes English transcripts while providing automatic fallbacks to available languages.

## Technology Stack

### Backend
- **Framework:** FastAPI 1.0.0
- **Server:** Uvicorn with auto-reload
- **Language:** Python 3.x
- **Core Libraries:**
  - youtube-transcript-api (transcript extraction)
  - yt-dlp (video metadata extraction)
  - pydantic (data validation)
  - requests (HTTP requests)
  - python-multipart (form data handling)
  - jinja2 (template support)
  - aiofiles (async file operations)

### Frontend
- **Languages:** HTML5, CSS3, vanilla JavaScript
- **Architecture:** Single-page application (SPA)
- **UI Framework:** Custom CSS with modern responsive design
- **JavaScript:** ES6+ with async/await patterns

### Tools & Deployment
- **Development:** Python virtual environment
- **Server:** Uvicorn development server
- **API Documentation:** Automatic OpenAPI/Swagger docs via FastAPI

## User Personas

### Primary User: Content Creators
- **Description:** YouTubers, podcasters, and video editors
- **Needs:** Quick access to video transcripts for subtitle creation, content repurposing, and editing workflows
- **Pain Points:** Manual transcription is time-consuming and expensive

### Secondary User: Researchers & Analysts
- **Description:** Academic researchers, market analysts, and content analysts
- **Needs:** Text-based analysis of video content, quotation extraction, and content categorization
- **Pain Points:** Need searchable, text format of video content for analysis tools

### Tertiary User: Students & Educators
- **Description:** Students taking online courses, educators creating materials
- **Needs:** Study materials, note-taking, and accessibility features
- **Pain Points:** Video content is not always accessible or searchable

### Quaternary User: Accessibility Advocates
- **Description:** Users requiring text alternatives to audio content
- **Needs:** Full transcript access for hearing-impaired users
- **Pain Points:** Not all videos have accurate closed captions

## Features

### Completed Features

- **YouTube URL Processing:** Comprehensive URL format support including standard URLs, youtu.be short URLs, embed URLs, shorts URLs, live URLs, and mobile URLs (Added 2024-01-08)
- **Video ID Extraction:** Robust video ID extraction with regex patterns and URL parsing fallbacks (Added 2024-01-08)
- **Transcript Extraction:** Multi-language transcript extraction with English priority and automatic fallbacks (Added 2024-01-08)
- **Chapter Detection:** Automatic chapter extraction from video metadata using yt-dlp integration (Added 2024-01-08)
- **Clean Transcript Formatting:** Text cleaning and formatting for improved readability (Added 2024-01-08)
- **Copy to Clipboard:** One-click transcript copying functionality (Added 2024-01-08)
- **Download Functionality:** Clean filename generation and text file download (Added 2024-01-08)
- **Responsive Web Interface:** Modern, mobile-friendly UI with loading states and error handling (Added 2024-01-08)
- **Toast Notifications:** User feedback system for success/error states (Added 2024-01-08)
- **URL Validation:** Client-side and server-side URL validation (Added 2024-01-08)
- **Video Metadata Display:** Title, duration, and extraction timestamp display (Added 2024-01-08)
- **Error Handling:** Comprehensive error handling with user-friendly messages (Added 2024-01-08)

### In-Progress Features
*None currently in development*

### Planned Features

- **Batch Processing:** Upload multiple YouTube URLs and process them in sequence
- **Additional Export Formats:** PDF, DOCX, and SRT subtitle file exports
- **Transcript Search:** Full-text search with highlighting within transcripts
- **User Authentication:** Account creation and transcript history management
- **API Rate Limiting:** Prevent abuse and ensure fair usage
- **Docker Deployment:** Containerized deployment for easy hosting
- **Advanced Filtering:** Language preference settings and transcript quality filters
- **Transcript Editing:** Basic editing capabilities for downloaded transcripts
- **Integration APIs:** REST API endpoints for third-party integrations

## Architecture

### System Architecture
- **Pattern:** Service-oriented architecture with clear separation of concerns
- **API Design:** RESTful API with FastAPI's automatic documentation
- **Concurrency:** Async/await patterns throughout for non-blocking operations
- **Static Serving:** FastAPI static file serving for frontend assets

### Core Services
- **TranscriptService:** Handles YouTube transcript extraction and text formatting
- **ChapterService:** Extracts chapter information from video metadata
- **URLExtractor:** Validates and extracts video IDs from various URL formats

### Database Schema
*Current version uses no persistent storage - all operations are stateless*

Future database schema (planned):
```sql
Users (user_id, email, created_at, subscription_type)
Transcripts (transcript_id, user_id, video_id, title, content, created_at)
ProcessingJobs (job_id, user_id, status, created_at, completed_at)
```

### API Structure

#### Current Endpoints
- `GET /` - Serve main application page
- `POST /api/transcript` - Extract transcript from YouTube URL
- `GET /api/health` - Health check endpoint
- `GET /static/*` - Static file serving

#### Request/Response Models
- **TranscriptRequest:** `{ url: string }`
- **TranscriptResponse:** `{ video_id, title, transcript, chapters, duration, extracted_at }`
- **ChapterData:** `{ title, start_time, end_time, timestamp }`
- **ErrorResponse:** `{ error, detail, timestamp }`

### Routing
- Single-page application with client-side routing
- Static file serving for CSS, JavaScript, and assets
- API routes under `/api/` prefix

### State Management
- Client-side: Vanilla JavaScript with class-based component management
- No complex state management library required due to simple application state
- Server-side: Stateless request/response cycle

## Authentication System
*Not currently implemented*

Planned implementation:
- JWT token-based authentication
- Session management for transcript history
- Rate limiting per authenticated user
- Guest access with limited functionality

## UI/UX Patterns

### Design System
- **Color Scheme:** Modern, accessible color palette with proper contrast ratios
- **Typography:** Clean, readable font stack with proper hierarchy
- **Layout:** Centered container with responsive grid system
- **Components:** Reusable button styles, form inputs, and notification system

### Interaction Patterns
- **Loading States:** Spinner animations during API calls
- **Error Handling:** Friendly error messages with retry options
- **Toast Notifications:** Non-intrusive success/error feedback
- **Progressive Enhancement:** Works without JavaScript for basic functionality

### Accessibility Features
- Proper ARIA labels and semantic HTML
- Keyboard navigation support
- Screen reader compatibility
- High contrast color scheme

## Business Rules

### Transcript Processing
- English language transcripts are prioritized
- Fallback order: Manual English → Generated English → Any available language
- Transcript cleaning removes timestamps and formatting artifacts
- Maximum processing time: 30 seconds per request

### URL Validation
- Support for all standard YouTube URL formats
- Video ID validation: 11-character alphanumeric with hyphens/underscores
- Reject invalid or non-YouTube URLs with clear error messages

### Content Restrictions
- Only publicly available YouTube videos
- Respects YouTube's transcript availability (no forced generation)
- No support for age-restricted or private videos

## Integration Points

### External Services
- **YouTube Transcript API:** Primary transcript extraction service
- **yt-dlp:** Video metadata extraction and validation
- **YouTube Platform:** Source of all video content and metadata

### Third-Party Dependencies
- All dependencies specified in requirements.txt
- Regular security updates required for youtube-transcript-api and yt-dlp

## Performance Considerations

### Optimization Strategies
- Async/await patterns prevent blocking operations
- Concurrent processing of metadata and transcript extraction
- Efficient text processing with minimal memory allocation
- Client-side caching of extracted transcripts

### Scalability
- Stateless architecture enables horizontal scaling
- Individual request isolation prevents cascade failures
- Future: Connection pooling and request queueing for high traffic

### Monitoring
- Basic error logging implemented
- Future: Performance metrics, request tracking, and usage analytics

## Environment Variables

### Current Configuration
*All configuration is currently hardcoded*

### Future Environment Variables
```
DATABASE_URL=postgresql://...
JWT_SECRET_KEY=...
YOUTUBE_API_KEY=... (if needed for enhanced features)
RATE_LIMIT_REQUESTS_PER_MINUTE=60
MAX_CONCURRENT_JOBS=10
```

## Testing Strategy

### Current Testing
*No automated tests currently implemented*

### Planned Testing Approach
- **Unit Tests:** Service-level testing with pytest
- **Integration Tests:** API endpoint testing with FastAPI test client
- **Frontend Tests:** JavaScript unit tests for key functions
- **E2E Tests:** Full user workflow testing with Playwright

### Test Coverage Goals
- 80% backend code coverage
- All API endpoints tested
- Critical user workflows covered in E2E tests

## Deployment

### Current Deployment
- Local development server via `python run.py`
- Uvicorn server with auto-reload enabled
- Static file serving from FastAPI

### Production Deployment (Planned)
- Docker containerization
- Reverse proxy setup (nginx)
- Process management (gunicorn/uvicorn workers)
- Environment-specific configuration
- Health monitoring and logging

### Infrastructure
- **Hosting:** Cloud platform (AWS, GCP, or DigitalOcean)
- **Database:** PostgreSQL for user data and transcript history
- **Caching:** Redis for frequently accessed transcripts
- **CDN:** CloudFlare for static asset delivery

## Constraints & Non-Goals

### Technical Constraints
- YouTube's transcript availability (cannot generate transcripts for videos without them)
- API rate limits from YouTube and transcript services
- Browser compatibility requirements (modern browsers only)
- File size limitations for very long videos

### Business Constraints
- No monetization features in current version
- No enterprise features or white-labeling
- Limited to YouTube platform only

### Explicit Non-Goals
- Video downloading or storage
- Transcript generation/AI transcription
- Social features or user communities
- Multi-language UI (English only)
- Real-time collaboration features

## Development Guidelines

### Code Style
- Python: Follow PEP 8 standards
- JavaScript: ES6+ with consistent naming conventions
- HTML/CSS: Semantic markup with BEM-style CSS classes

### Best Practices
- Async/await for all I/O operations
- Comprehensive error handling with user-friendly messages
- Type hints for all Python functions
- JSDoc comments for complex JavaScript functions
- Responsive design principles for all UI components

### Version Control
- Feature branch workflow
- Descriptive commit messages
- Regular dependency updates
- Security patch priority

### Documentation
- API documentation via FastAPI's automatic OpenAPI generation
- Code comments for complex business logic
- README updates for deployment and development setup

---

*Document created: 2025-01-11*  
*Last updated: 2025-01-11*