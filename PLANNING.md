# PLANNING.md

## Project Overview

**Name:** YouTube Transcriber  
**Purpose:** A standalone command-line application for extracting YouTube video transcripts with support for multiple URL formats, batch processing, and flexible output options  
**Status:** Production-ready  
**Version:** 2.0.0  

The YouTube Transcriber is a simple, efficient CLI tool that allows users to extract transcripts from YouTube videos directly from their terminal. It supports various YouTube URL formats, batch processing, and prioritizes English transcripts while providing automatic fallbacks to available languages.

## Technology Stack

### Core Application
- **Type:** Command-line interface (CLI)
- **Language:** Python 3.x
- **Architecture:** Standalone single-file application
- **Core Libraries:**
  - youtube-transcript-api (transcript extraction)
  - yt-dlp (video metadata extraction)

### Tools & Distribution
- **Development:** Python virtual environment
- **Execution:** Direct Python script execution
- **Dependencies:** Minimal - only 2 external libraries

## User Personas

### Primary User: Developers & Power Users
- **Description:** Software developers, data scientists, and technical users comfortable with command-line tools
- **Needs:** Quick, automated transcript extraction for processing pipelines, research, and analysis
- **Pain Points:** Need scriptable, batch-processable solution without GUI overhead

### Secondary User: Content Creators
- **Description:** YouTubers, podcasters, and video editors who prefer command-line workflows
- **Needs:** Batch processing of multiple videos, automated filename generation, scriptable workflows
- **Pain Points:** Manual transcription is time-consuming, need automation for large volumes

### Tertiary User: Researchers & Analysts
- **Description:** Academic researchers, market analysts requiring programmatic access to transcript data
- **Needs:** Batch processing capabilities, clean text output for analysis pipelines, metadata extraction
- **Pain Points:** Need to process large datasets of videos efficiently

### Quaternary User: System Administrators
- **Description:** IT professionals integrating transcript extraction into larger systems
- **Needs:** Reliable, scriptable tool that can be integrated into automated workflows and cron jobs
- **Pain Points:** Need minimal dependencies and reliable error handling for production systems

## Features

### Completed Features

- **YouTube URL Processing:** Comprehensive URL format support including standard URLs, youtu.be short URLs, embed URLs, shorts URLs, live URLs, and mobile URLs (Converted 2025-01-11)
- **Video ID Extraction:** Robust video ID extraction with regex patterns and URL parsing fallbacks (Converted 2025-01-11)
- **Transcript Extraction:** Multi-language transcript extraction with English priority and automatic fallbacks (Converted 2025-01-11)
- **Clean Transcript Formatting:** Advanced text cleaning and paragraph formatting for improved readability (Enhanced 2025-01-11)
- **Batch Processing:** Process multiple URLs from input file with progress tracking (Added 2025-01-11)
- **Flexible Output Options:** Console output, file output, or automatic filename generation (Added 2025-01-11)
- **Video Metadata Integration:** Optional video metadata (title, duration, uploader) in output (Added 2025-01-11)
- **Command-line Interface:** Full argparse-based CLI with comprehensive options (Added 2025-01-11)
- **Progress Tracking:** Real-time progress indication for batch operations (Added 2025-01-11)
- **Error Handling:** Comprehensive error handling with clear CLI error messages (Enhanced 2025-01-11)
- **Quiet Mode:** Suppress progress messages for scripting use cases (Added 2025-01-11)
- **Auto-naming:** Automatic filename generation based on video titles (Added 2025-01-11)

### In-Progress Features
*None currently in development*

### Planned Features

- **Additional Export Formats:** SRT subtitle file export, JSON structured output
- **Advanced Filtering:** Language preference configuration, transcript quality filtering
- **Rate Limiting Controls:** Built-in delays and retry logic for YouTube API limits
- **Configuration File Support:** YAML/JSON config files for default settings
- **Logging System:** Structured logging for debugging and audit trails
- **Plugin Architecture:** Extensible formatting and output plugins
- **Docker Support:** Containerized version for deployment environments
- **Performance Optimization:** Concurrent processing for batch operations
- **Advanced Error Recovery:** Retry mechanisms and graceful degradation

## Architecture

### System Architecture
- **Pattern:** Single-file CLI application with modular class design
- **Execution Model:** Direct Python script execution with argument parsing
- **Processing:** Synchronous processing with error handling and progress tracking
- **Storage:** No persistent storage - stateless operations only

### Core Classes
- **YouTubeTranscriber:** Main orchestrator class handling the complete workflow
- **URLExtractor:** Validates and extracts video IDs from various YouTube URL formats
- **SimpleFormatter:** Advanced text formatting and paragraph structuring

### Data Flow
1. URL/batch file input via command line
2. Video ID extraction and validation
3. Metadata retrieval (optional)
4. Transcript extraction with language fallbacks
5. Text formatting and paragraph structuring
6. Output to console or file(s)

### CLI Interface
- **Argument Parsing:** argparse-based command-line interface
- **Input Methods:** Single URL, video ID, or batch file processing
- **Output Options:** Console, specific file, auto-generated filename, or directory
- **Configuration:** Command-line flags for metadata, quiet mode, etc.

### Error Handling
- Graceful failure with informative error messages
- Continue-on-error for batch processing
- Detailed error reporting to stderr
- Exit codes for scripting integration

## Configuration System
*Currently command-line only*

Planned configuration options:
- Configuration file support (YAML/JSON)
- Environment variable support
- User-specific default settings
- Language preference configuration

## CLI UX Patterns

### Command Design
- **Intuitive Arguments:** Clear, logical argument structure
- **Help System:** Comprehensive help text with examples
- **Progress Feedback:** Real-time progress indication for long operations
- **Error Messages:** Clear, actionable error messages with suggestions

### Output Patterns
- **Structured Output:** Consistent formatting for metadata and transcripts
- **Quiet Mode:** Suppressed output for scripting scenarios
- **Batch Summaries:** Comprehensive success/failure reporting
- **Flexible Formatting:** Optional metadata inclusion/exclusion

### Accessibility Features
- Clear error messages and status updates
- Progress indication for batch operations
- Consistent exit codes for scripting
- Standard stream usage (stdout/stderr)

## Business Rules

### Transcript Processing
- English language transcripts are prioritized
- Fallback order: English → Manual English → Generated English → Any available language
- Advanced text formatting creates natural paragraph breaks
- Sentence-level intelligent paragraph grouping
- Automatic text cleaning and capitalization
- No timeout limits for individual video processing

### URL Validation
- Support for all standard YouTube URL formats
- Video ID validation: 11-character alphanumeric with hyphens/underscores
- Reject invalid or non-YouTube URLs with clear error messages

### Content Restrictions
- Only publicly available YouTube videos with existing transcripts
- Respects YouTube's transcript availability (no forced generation)
- No support for age-restricted or private videos
- Batch processing continues on individual failures

## Integration Points

### External Services
- **YouTube Transcript API:** Primary transcript extraction service
- **yt-dlp:** Video metadata extraction and validation
- **YouTube Platform:** Source of all video content and metadata

### System Integration
- **Command Line:** Standard CLI interface for shell integration
- **Scripting:** Exit codes and error handling for automation
- **File System:** Direct file output for integration with other tools
- **Batch Processing:** File-based input for large-scale operations

### Third-Party Dependencies
- Minimal dependencies: only youtube-transcript-api and yt-dlp
- Regular security updates required for both dependencies

## Performance Considerations

### Optimization Strategies
- Synchronous processing with efficient resource usage
- Minimal memory allocation for text processing
- Efficient regex-based text formatting
- Direct file I/O without intermediate caching

### Scalability
- Single-process CLI design optimized for individual use
- Stateless operation enables parallel execution of multiple instances
- Batch processing handles large datasets efficiently
- Future: Concurrent processing for batch operations

### Monitoring
- Error output to stderr for monitoring integration
- Exit codes for success/failure detection
- Progress reporting for batch operations
- Future: Structured logging and performance metrics

## Configuration Options

### Current Configuration
*All configuration via command-line arguments*

### Future Configuration Support
```
YOUTUBE_TRANSCRIBER_LANGUAGE_PREFERENCE=en
YOUTUBE_TRANSCRIBER_OUTPUT_DIR=./transcripts
YOUTUBE_TRANSCRIBER_INCLUDE_METADATA=true
YOUTUBE_TRANSCRIBER_QUIET_MODE=false
YOUTUBE_TRANSCRIBER_RATE_LIMIT_DELAY=1
```

## Testing Strategy

### Current Testing
*Manual testing with various YouTube URL formats*

### Planned Testing Approach
- **Unit Tests:** Class-level testing with pytest for URL extraction, formatting
- **Integration Tests:** End-to-end CLI testing with real YouTube videos
- **Batch Tests:** Large dataset processing validation
- **Error Handling Tests:** Network failures, invalid URLs, missing transcripts

### Test Coverage Goals
- 80% code coverage for core classes
- All URL format patterns tested
- Batch processing workflows validated
- Error scenarios comprehensively covered

## Distribution

### Current Distribution
- Direct Python script execution: `python youtube_transcriber.py`
- Virtual environment with minimal dependencies
- Single-file application for easy deployment

### Distribution Options (Planned)
- **PyPI Package:** pip-installable package with console script
- **Docker Container:** Containerized version for consistent environments
- **Standalone Binary:** PyInstaller-based executable for systems without Python
- **System Package:** Distribution-specific packages (deb, rpm)

### Deployment Scenarios
- **Developer Workstation:** Direct script execution in virtual environment
- **CI/CD Pipeline:** Containerized batch processing
- **Server Automation:** cron-based scheduled transcript extraction
- **Data Processing:** Integration with larger data processing workflows

## Constraints & Non-Goals

### Technical Constraints
- YouTube's transcript availability (cannot generate transcripts for videos without them)
- API rate limits from YouTube and transcript services
- Python 3.8+ requirement for modern language features
- Memory usage scales with transcript length and batch size

### Usage Constraints
- Command-line interface requires terminal familiarity
- No GUI for users preferring graphical interfaces
- Limited to YouTube platform only
- Single-threaded processing (no concurrent downloads)

### Explicit Non-Goals
- Video downloading or storage
- Transcript generation/AI transcription
- Graphical user interface (GUI)
- Web server or API functionality
- Multi-user or collaborative features
- Real-time processing or streaming

## Development Guidelines

### Code Style
- Python: Follow PEP 8 standards
- Type hints for all function parameters and return values
- Docstrings for all classes and public methods
- Consistent error handling patterns

### Best Practices
- Comprehensive error handling with clear CLI messages
- Type hints for all Python functions and methods
- Modular class design with single responsibility principle
- Graceful degradation for network and API failures
- Clear separation between data processing and I/O operations

### Version Control
- Feature branch workflow
- Descriptive commit messages
- Regular dependency updates
- Security patch priority

### Documentation
- Comprehensive CLI help text with examples
- Code comments for complex text processing logic
- README with detailed usage examples and troubleshooting
- Inline docstrings for all public methods

---

*Document created: 2025-01-11*  
*Last updated: 2025-01-11 (Converted to CLI architecture)*