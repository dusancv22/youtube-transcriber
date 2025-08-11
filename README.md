# YouTube Transcriber - Standalone CLI Application

A simple, standalone Python application to extract transcripts from YouTube videos. No web server required - just run it directly from your terminal!

## Features

- Extract transcripts from any YouTube video with closed captions
- Support for multiple YouTube URL formats (standard, shorts, live, embedded, youtu.be)
- Batch processing - extract transcripts from multiple videos at once
- Automatic language detection with English preference
- Clean, formatted output with natural paragraph breaks
- Optional video metadata (title, duration, uploader)
- Flexible output options (console, file, or auto-generated filenames)

## Installation

1. Clone or download this repository
2. Install the minimal dependencies:

```bash
pip install -r requirements.txt
```

That's it! Only 2 dependencies:
- `youtube-transcript-api` - for extracting transcripts
- `yt-dlp` - for fetching video metadata

## Usage

### Basic Usage

Extract transcript and display in console:
```bash
python youtube_transcriber.py https://www.youtube.com/watch?v=VIDEO_ID
```

### Save to File

Save transcript to a specific file:
```bash
python youtube_transcriber.py https://youtu.be/VIDEO_ID -o transcript.txt
```

Auto-generate filename based on video title:
```bash
python youtube_transcriber.py VIDEO_ID -o auto
```

### Batch Processing

Create a file with URLs (one per line):
```text
# urls.txt
https://www.youtube.com/watch?v=VIDEO1
https://youtu.be/VIDEO2
https://youtube.com/shorts/VIDEO3
```

Process all URLs and save to a directory:
```bash
python youtube_transcriber.py -b urls.txt -d output_folder
```

### Additional Options

Exclude metadata from output:
```bash
python youtube_transcriber.py URL --no-metadata
```

Suppress progress messages:
```bash
python youtube_transcriber.py URL -q --quiet
```

### Supported URL Formats

The tool supports all common YouTube URL formats:
- Standard: `https://www.youtube.com/watch?v=VIDEO_ID`
- Short: `https://youtu.be/VIDEO_ID`
- Shorts: `https://youtube.com/shorts/VIDEO_ID`
- Live: `https://www.youtube.com/live/VIDEO_ID`
- Embed: `https://www.youtube.com/embed/VIDEO_ID`
- Mobile: `https://m.youtube.com/watch?v=VIDEO_ID`
- Direct video ID: `VIDEO_ID`

## Command Line Options

```
positional arguments:
  url                   YouTube URL or video ID

options:
  -h, --help            Show help message
  -o, --output          Output file (use "auto" for automatic naming)
  -d, --output-dir      Output directory for batch processing
  -b, --batch           Process URLs from file (one per line)
  --no-metadata         Exclude video metadata from output
  -q, --quiet           Suppress progress messages
```

## Examples

### Example 1: Quick Transcript
```bash
python youtube_transcriber.py dQw4w9WgXcQ
```

### Example 2: Save with Metadata
```bash
python youtube_transcriber.py https://www.youtube.com/watch?v=dQw4w9WgXcQ -o "rick_roll_transcript.txt"
```

### Example 3: Batch Processing
```bash
# Process multiple videos and save each to a separate file
python youtube_transcriber.py -b video_list.txt -d transcripts/
```

### Example 4: Clean Output
```bash
# Just the transcript, no metadata, saved to file
python youtube_transcriber.py VIDEO_ID --no-metadata -o clean.txt
```

## Output Format

With metadata (default):
```
================================================================================
Title: Video Title Here
Uploader: Channel Name
Duration: 10:35
URL: https://www.youtube.com/watch?v=VIDEO_ID
================================================================================

This is the transcript text formatted into natural paragraphs. Each paragraph
contains multiple sentences grouped logically together.

Another paragraph continues here with the next part of the transcript...
```

Without metadata (`--no-metadata`):
```
This is the transcript text formatted into natural paragraphs. Each paragraph
contains multiple sentences grouped logically together.

Another paragraph continues here with the next part of the transcript...
```

## Error Handling

The tool provides clear error messages:
- Invalid URL format
- Video without available transcripts
- Network issues or YouTube blocking
- File access problems

## Tips

1. **Auto-naming**: Use `-o auto` to automatically generate filenames based on video titles
2. **Batch files**: Lines starting with `#` in batch files are treated as comments
3. **Language fallback**: If English transcript isn't available, the tool will use the first available language
4. **Rate limiting**: If processing many videos, add delays between requests to avoid YouTube blocking

## Troubleshooting

### "No transcript available"
- The video doesn't have closed captions enabled
- The video is private or age-restricted
- Live stream is still ongoing (transcripts only available after stream ends)

### "YouTube is blocking requests"
- You've made too many requests - wait a while before trying again
- Consider using a VPN or proxy
- Add delays between batch requests

### "Could not extract video ID"
- Check the URL format is correct
- Ensure the video still exists and is public

## Requirements

- Python 3.8+
- youtube-transcript-api
- yt-dlp

## License

This is a standalone tool for personal use. Please respect YouTube's Terms of Service and content creators' rights when using extracted transcripts.