# YouTube Transcriber

A web application for transcribing YouTube videos with FastAPI backend and clean frontend interface.

## Features

- Extract transcripts from YouTube videos
- Clean and format transcripts
- Chapter detection and organization
- Modern web interface

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python run.py
   ```

2. Open your browser and navigate to `http://localhost:8000`

3. Enter a YouTube URL to get the transcript

## API Endpoints

- `GET /` - Web interface
- `POST /api/transcript` - Get transcript for YouTube URL
- `GET /api/health` - Health check endpoint

## Requirements

- Python 3.8+
- FastAPI
- yt-dlp
- youtube-transcript-api