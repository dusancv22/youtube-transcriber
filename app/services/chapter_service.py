"""
Service for extracting and processing video chapters
"""

import asyncio
import re
from typing import List, Optional
import yt_dlp
import logging
from ..models.transcript import ChapterData

logger = logging.getLogger(__name__)

class ChapterService:
    """Service for extracting video chapter information"""
    
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extractaudio': False,
        }
    
    async def get_chapters(self, video_id: str) -> List[ChapterData]:
        """
        Extract chapter information from a YouTube video
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            List of ChapterData objects
        """
        try:
            # Try to get chapters from video metadata
            chapters = await self._extract_chapters_from_metadata(video_id)
            
            if not chapters:
                # Try to extract chapters from description
                chapters = await self._extract_chapters_from_description(video_id)
            
            return chapters
            
        except Exception as e:
            logger.error(f"Error getting chapters for video {video_id}: {str(e)}")
            return []
    
    async def _extract_chapters_from_metadata(self, video_id: str) -> List[ChapterData]:
        """Extract chapters from video metadata"""
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                loop = asyncio.get_event_loop()
                info = await loop.run_in_executor(
                    None,
                    lambda: ydl.extract_info(url, download=False)
                )
                
                chapters_data = info.get('chapters', [])
                chapters = []
                
                for i, chapter in enumerate(chapters_data):
                    start_time = int(chapter.get('start_time', 0))
                    end_time = int(chapter.get('end_time', 0)) if chapter.get('end_time') else None
                    
                    # Set end_time for previous chapter if not set
                    if i > 0 and chapters[-1].end_time is None:
                        chapters[-1].end_time = start_time
                    
                    chapter_data = ChapterData(
                        title=chapter.get('title', f'Chapter {i+1}'),
                        start_time=start_time,
                        end_time=end_time,
                        timestamp=self._format_timestamp(start_time)
                    )
                    chapters.append(chapter_data)
                
                return chapters
                
        except Exception as e:
            logger.error(f"Error extracting chapters from metadata: {str(e)}")
            return []
    
    async def _extract_chapters_from_description(self, video_id: str) -> List[ChapterData]:
        """Extract chapters from video description using pattern matching"""
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                loop = asyncio.get_event_loop()
                info = await loop.run_in_executor(
                    None,
                    lambda: ydl.extract_info(url, download=False)
                )
                
                description = info.get('description', '')
                if not description:
                    return []
                
                chapters = self._parse_chapters_from_text(description)
                return chapters
                
        except Exception as e:
            logger.error(f"Error extracting chapters from description: {str(e)}")
            return []
    
    def _parse_chapters_from_text(self, text: str) -> List[ChapterData]:
        """Parse chapter timestamps and titles from text"""
        chapters = []
        
        # Patterns for different timestamp formats
        patterns = [
            r'(\d{1,2}:\d{2}(?::\d{2})?)\s*[-–—]\s*(.+?)(?=\n|\d{1,2}:\d{2}|$)',
            r'(\d{1,2}:\d{2}(?::\d{2})?)\s+(.+?)(?=\n|\d{1,2}:\d{2}|$)',
            r'(\d{1,2}:\d{2}(?::\d{2})?)\s*[:\-–—]\s*(.+?)(?=\n|\d{1,2}:\d{2}|$)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.MULTILINE | re.IGNORECASE)
            
            if matches:
                for i, (timestamp_str, title) in enumerate(matches):
                    start_time = self._parse_timestamp(timestamp_str.strip())
                    title = title.strip()
                    
                    # Clean up the title
                    title = re.sub(r'[\n\r\t]+', ' ', title)
                    title = re.sub(r'\s+', ' ', title)
                    title = title.strip()
                    
                    if start_time is not None and title:
                        # Set end_time for previous chapter
                        if chapters and chapters[-1].end_time is None:
                            chapters[-1].end_time = start_time
                        
                        chapter_data = ChapterData(
                            title=title,
                            start_time=start_time,
                            end_time=None,  # Will be set by next chapter or left as None for last chapter
                            timestamp=timestamp_str
                        )
                        chapters.append(chapter_data)
                
                # If we found chapters, break and return them
                if chapters:
                    break
        
        return chapters
    
    def _parse_timestamp(self, timestamp_str: str) -> Optional[int]:
        """Parse timestamp string to seconds"""
        try:
            parts = timestamp_str.split(':')
            
            if len(parts) == 2:  # MM:SS
                minutes, seconds = map(int, parts)
                return minutes * 60 + seconds
            elif len(parts) == 3:  # HH:MM:SS
                hours, minutes, seconds = map(int, parts)
                return hours * 3600 + minutes * 60 + seconds
            else:
                return None
                
        except (ValueError, AttributeError):
            return None
    
    def _format_timestamp(self, seconds: int) -> str:
        """Format seconds to timestamp string"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"