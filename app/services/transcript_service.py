"""
Service for handling YouTube transcript extraction
"""

import asyncio
from typing import Dict, Optional
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import yt_dlp
import logging

logger = logging.getLogger(__name__)

class TranscriptService:
    """Service for extracting YouTube video transcripts"""
    
    def __init__(self):
        self.formatter = TextFormatter()
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extractaudio': False,
            'extract_flat': True,
        }
    
    async def get_transcript(self, video_id: str) -> Dict[str, any]:
        """
        Extract transcript and metadata for a YouTube video
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Dictionary containing transcript, title, and duration
        """
        try:
            # Get video metadata
            metadata = await self._get_video_metadata(video_id)
            
            # Get transcript
            transcript_text = await self._extract_transcript(video_id)
            
            return {
                "transcript": transcript_text,
                "title": metadata.get("title", ""),
                "duration": metadata.get("duration", 0),
                "description": metadata.get("description", ""),
                "upload_date": metadata.get("upload_date", ""),
                "uploader": metadata.get("uploader", "")
            }
            
        except Exception as e:
            logger.error(f"Error getting transcript for video {video_id}: {str(e)}")
            raise Exception(f"Failed to extract transcript: {str(e)}")
    
    async def _extract_transcript(self, video_id: str) -> str:
        """Extract transcript text from YouTube video"""
        try:
            # Create API instance (correct usage)
            api = YouTubeTranscriptApi()
            
            # Get transcript list for the video
            transcript_list = api.list(video_id)
            
            # Try to find English transcript first
            transcript = None
            try:
                transcript = transcript_list.find_transcript(['en'])
                logger.info(f"Found English transcript for video {video_id}")
            except Exception:
                try:
                    # Try manually created transcript in English
                    transcript = transcript_list.find_manually_created_transcript(['en'])
                    logger.info(f"Found manually created English transcript for video {video_id}")
                except Exception:
                    try:
                        # Try generated transcript in English
                        transcript = transcript_list.find_generated_transcript(['en'])
                        logger.info(f"Found generated English transcript for video {video_id}")
                    except Exception:
                        # Get first available transcript
                        for t in transcript_list:
                            transcript = t
                            logger.info(f"Using available transcript in language: {transcript.language}")
                            break
            
            if not transcript:
                raise Exception("No transcript available for this video")
            
            # Fetch the transcript data
            transcript_data = transcript.fetch()
            
            # Format the transcript
            formatted_transcript = self.formatter.format_transcript(transcript_data)
            
            # Clean up the transcript
            cleaned_transcript = self._clean_transcript(formatted_transcript)
            
            return cleaned_transcript
            
        except Exception as e:
            logger.error(f"Error extracting transcript for video {video_id}: {str(e)}")
            raise Exception(f"Failed to extract transcript: {str(e)}")
    
    async def _get_video_metadata(self, video_id: str) -> Dict[str, any]:
        """Get video metadata using yt-dlp"""
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # Run in thread to avoid blocking
                loop = asyncio.get_event_loop()
                info = await loop.run_in_executor(
                    None, 
                    lambda: ydl.extract_info(url, download=False)
                )
                
                return {
                    "title": info.get("title", ""),
                    "duration": info.get("duration", 0),
                    "description": info.get("description", ""),
                    "upload_date": info.get("upload_date", ""),
                    "uploader": info.get("uploader", ""),
                    "view_count": info.get("view_count", 0),
                    "like_count": info.get("like_count", 0),
                }
                
        except Exception as e:
            logger.error(f"Error getting video metadata: {str(e)}")
            return {"title": "", "duration": 0}
    
    def _clean_transcript(self, transcript: str) -> str:
        """Clean and format transcript text"""
        if not transcript:
            return ""
        
        # Basic cleaning
        lines = transcript.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('[') and not line.startswith('('):
                # Remove excessive whitespace
                line = ' '.join(line.split())
                cleaned_lines.append(line)
        
        # Join with proper spacing
        cleaned_transcript = '\n\n'.join(cleaned_lines)
        
        return cleaned_transcript