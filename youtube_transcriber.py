#!/usr/bin/env python3
"""
YouTube Transcriber - Standalone CLI Application
Extract transcripts from YouTube videos with support for multiple URL formats.
"""

import argparse
import sys
import os
import re
from typing import Dict, List, Optional
from urllib.parse import urlparse, parse_qs
from datetime import datetime

from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp


class URLExtractor:
    """Extract YouTube video IDs from various URL formats"""
    
    def __init__(self):
        self.url_patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
            r'(?:https?://)?youtu\.be/([a-zA-Z0-9_-]{11})',
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})',
            r'(?:https?://)?(?:www\.)?youtube\.com/shorts/([a-zA-Z0-9_-]{11})',
            r'(?:https?://)?(?:www\.)?youtube\.com/live/([a-zA-Z0-9_-]{11})',
            r'(?:https?://)?m\.youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
            r'^([a-zA-Z0-9_-]{11})$'
        ]
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract YouTube video ID from URL"""
        if not url:
            return None
        
        url = url.strip()
        
        # Try pattern matching
        for pattern in self.url_patterns:
            match = re.search(pattern, url, re.IGNORECASE)
            if match:
                video_id = match.group(1)
                if self._is_valid_video_id(video_id):
                    return video_id
        
        # Try URL parsing
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            parsed_url = urlparse(url)
            
            if parsed_url.hostname in ['www.youtube.com', 'youtube.com', 'm.youtube.com']:
                if parsed_url.path == '/watch':
                    query_params = parse_qs(parsed_url.query)
                    video_id = query_params.get('v', [None])[0]
                    if video_id and self._is_valid_video_id(video_id):
                        return video_id
                elif parsed_url.path.startswith('/embed/'):
                    video_id = parsed_url.path.split('/embed/')[1].split('?')[0]
                    if self._is_valid_video_id(video_id):
                        return video_id
                elif parsed_url.path.startswith('/shorts/'):
                    video_id = parsed_url.path.split('/shorts/')[1].split('?')[0]
                    if self._is_valid_video_id(video_id):
                        return video_id
                elif parsed_url.path.startswith('/live/'):
                    video_id = parsed_url.path.split('/live/')[1].split('?')[0]
                    if self._is_valid_video_id(video_id):
                        return video_id
            elif parsed_url.hostname == 'youtu.be':
                video_id = parsed_url.path[1:]
                if self._is_valid_video_id(video_id):
                    return video_id
        except Exception:
            pass
        
        return None
    
    def _is_valid_video_id(self, video_id: str) -> bool:
        """Validate YouTube video ID format"""
        if not video_id:
            return False
        return bool(re.match(r'^[a-zA-Z0-9_-]{11}$', video_id))


class SimpleFormatter:
    """Format transcript segments into readable paragraphs"""
    
    def format_transcript(self, segments: List) -> str:
        """Format transcript segments into natural paragraphs"""
        if not segments:
            return ""
        
        all_text = []
        
        for segment in segments:
            if hasattr(segment, 'text'):
                text = segment.text
            elif isinstance(segment, dict):
                text = segment.get('text', '')
            else:
                text = str(segment)
            
            text = text.replace('\n', ' ').strip()
            text = re.sub(r'\[.*?\]', '', text).strip()
            
            if text:
                all_text.append(text)
        
        full_text = ' '.join(all_text)
        full_text = re.sub(r'\s+', ' ', full_text)
        
        sentences = re.split(r'(?<=[.!?])\s+', full_text)
        
        if len(sentences) <= 3 and len(full_text) > 200:
            words = full_text.split()
            sentences = []
            current_sentence = []
            
            for i, word in enumerate(words):
                current_sentence.append(word)
                
                if len(current_sentence) >= 15:
                    sentence_text = ' '.join(current_sentence)
                    
                    if i + 1 < len(words) and words[i + 1][0].isupper():
                        sentences.append(sentence_text)
                        current_sentence = []
                    elif len(current_sentence) >= 20:
                        sentences.append(sentence_text)
                        current_sentence = []
            
            if current_sentence:
                sentences.append(' '.join(current_sentence))
        
        paragraphs = []
        current_paragraph = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            current_paragraph.append(sentence)
            paragraph_text = ' '.join(current_paragraph)
            
            should_break = False
            
            if len(current_paragraph) >= 4:
                should_break = True
            elif len(paragraph_text) > 500 and len(current_paragraph) >= 2:
                should_break = True
            elif sentence.lower().startswith(('now ', 'next,', 'however,', 'but ', 'so ', 
                                             'therefore', 'furthermore', 'additionally', 
                                             'finally', 'in conclusion', 'let me', "let's", 
                                             'okay', 'alright', 'well,')):
                if len(current_paragraph) > 1:
                    current_paragraph.pop()
                    if current_paragraph:
                        paragraphs.append(' '.join(current_paragraph))
                    current_paragraph = [sentence]
                    should_break = False
            
            if should_break:
                paragraphs.append(paragraph_text)
                current_paragraph = []
        
        if current_paragraph:
            paragraphs.append(' '.join(current_paragraph))
        
        formatted_paragraphs = []
        for para in paragraphs:
            para = para.strip()
            if para:
                para = para[0].upper() + para[1:] if len(para) > 1 else para.upper()
                if not para[-1] in '.!?':
                    para += '.'
                formatted_paragraphs.append(para)
        
        return '\n\n'.join(formatted_paragraphs)


class YouTubeTranscriber:
    """Main transcriber class that orchestrates the extraction process"""
    
    def __init__(self):
        self.url_extractor = URLExtractor()
        self.formatter = SimpleFormatter()
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
    
    def get_video_metadata(self, video_id: str) -> Dict:
        """Get video metadata using yt-dlp"""
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    "title": info.get("title", "Untitled"),
                    "duration": info.get("duration", 0),
                    "uploader": info.get("uploader", "Unknown"),
                    "upload_date": info.get("upload_date", ""),
                    "view_count": info.get("view_count", 0),
                }
        except Exception as e:
            print(f"Warning: Could not fetch video metadata: {e}", file=sys.stderr)
            return {"title": "Unknown Title", "duration": 0}
    
    def extract_transcript(self, video_id: str) -> Optional[str]:
        """Extract transcript from YouTube video"""
        try:
            api = YouTubeTranscriptApi()
            transcript_list = api.list(video_id)
            
            transcript = None
            try:
                transcript = transcript_list.find_transcript(['en'])
            except:
                try:
                    transcript = transcript_list.find_manually_created_transcript(['en'])
                except:
                    try:
                        transcript = transcript_list.find_generated_transcript(['en'])
                    except:
                        for t in transcript_list:
                            transcript = t
                            print(f"Using transcript in language: {transcript.language}", file=sys.stderr)
                            break
            
            if not transcript:
                return None
            
            transcript_data = transcript.fetch()
            formatted_transcript = self.formatter.format_transcript(transcript_data)
            return formatted_transcript
            
        except Exception as e:
            print(f"Error extracting transcript: {e}", file=sys.stderr)
            return None
    
    def process_url(self, url: str, output_file: Optional[str] = None, 
                   include_metadata: bool = True, quiet: bool = False) -> bool:
        """Process a single YouTube URL"""
        if not quiet:
            print(f"Processing: {url}")
        
        video_id = self.url_extractor.extract_video_id(url)
        if not video_id:
            print(f"Error: Could not extract video ID from URL: {url}", file=sys.stderr)
            return False
        
        if not quiet:
            print(f"Video ID: {video_id}")
        
        # Get metadata
        metadata = self.get_video_metadata(video_id) if include_metadata else {}
        
        # Extract transcript
        transcript = self.extract_transcript(video_id)
        if not transcript:
            print(f"Error: No transcript available for video ID: {video_id}", file=sys.stderr)
            return False
        
        # Prepare output
        output_lines = []
        
        if include_metadata and metadata:
            output_lines.append("=" * 80)
            output_lines.append(f"Title: {metadata.get('title', 'Unknown')}")
            output_lines.append(f"Uploader: {metadata.get('uploader', 'Unknown')}")
            if metadata.get('duration'):
                duration = metadata['duration']
                hours = duration // 3600
                minutes = (duration % 3600) // 60
                seconds = duration % 60
                if hours > 0:
                    output_lines.append(f"Duration: {hours:02d}:{minutes:02d}:{seconds:02d}")
                else:
                    output_lines.append(f"Duration: {minutes:02d}:{seconds:02d}")
            output_lines.append(f"URL: https://www.youtube.com/watch?v={video_id}")
            output_lines.append("=" * 80)
            output_lines.append("")
        
        output_lines.append(transcript)
        
        output_text = '\n'.join(output_lines)
        
        # Save or print
        if output_file:
            # Generate filename if needed
            if output_file == 'auto':
                safe_title = re.sub(r'[^\w\s-]', '', metadata.get('title', 'transcript'))
                safe_title = re.sub(r'[-\s]+', '-', safe_title)[:100]
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_file = f"{safe_title}_{timestamp}.txt"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output_text)
            
            if not quiet:
                print(f"Transcript saved to: {output_file}")
        else:
            print(output_text)
        
        return True
    
    def process_batch(self, urls: List[str], output_dir: Optional[str] = None,
                     include_metadata: bool = True, quiet: bool = False) -> Dict[str, bool]:
        """Process multiple YouTube URLs"""
        results = {}
        
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for i, url in enumerate(urls, 1):
            if not quiet:
                print(f"\n[{i}/{len(urls)}] ", end="")
            
            if output_dir:
                output_file = os.path.join(output_dir, 'auto')
            else:
                output_file = None
            
            success = self.process_url(url, output_file, include_metadata, quiet)
            results[url] = success
        
        return results


def main():
    parser = argparse.ArgumentParser(
        description='Extract transcripts from YouTube videos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://www.youtube.com/watch?v=VIDEO_ID
  %(prog)s VIDEO_ID -o transcript.txt
  %(prog)s https://youtu.be/VIDEO_ID --no-metadata
  %(prog)s -b urls.txt -d output_folder
  %(prog)s https://youtube.com/live/VIDEO_ID -o auto
        """
    )
    
    parser.add_argument('url', nargs='?', help='YouTube URL or video ID')
    parser.add_argument('-o', '--output', help='Output file (use "auto" for automatic naming)')
    parser.add_argument('-d', '--output-dir', help='Output directory for batch processing')
    parser.add_argument('-b', '--batch', help='Process URLs from file (one per line)')
    parser.add_argument('--no-metadata', action='store_true', help='Exclude video metadata from output')
    parser.add_argument('-q', '--quiet', action='store_true', help='Suppress progress messages')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.url and not args.batch:
        parser.error('Either URL or --batch file must be provided')
    
    if args.url and args.batch:
        parser.error('Cannot specify both URL and --batch')
    
    # Initialize transcriber
    transcriber = YouTubeTranscriber()
    
    # Process batch or single URL
    if args.batch:
        if not os.path.exists(args.batch):
            print(f"Error: Batch file not found: {args.batch}", file=sys.stderr)
            sys.exit(1)
        
        with open(args.batch, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if not urls:
            print("Error: No URLs found in batch file", file=sys.stderr)
            sys.exit(1)
        
        print(f"Processing {len(urls)} URLs from {args.batch}")
        results = transcriber.process_batch(
            urls, 
            args.output_dir,
            not args.no_metadata,
            args.quiet
        )
        
        # Print summary
        successful = sum(1 for success in results.values() if success)
        failed = len(results) - successful
        
        print(f"\n{'='*50}")
        print(f"Processed: {len(results)} URLs")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        
        if failed > 0:
            print("\nFailed URLs:")
            for url, success in results.items():
                if not success:
                    print(f"  - {url}")
        
        sys.exit(0 if failed == 0 else 1)
    else:
        # Process single URL
        success = transcriber.process_url(
            args.url,
            args.output,
            not args.no_metadata,
            args.quiet
        )
        
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()