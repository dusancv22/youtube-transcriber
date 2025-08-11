"""
Service for extracting and validating YouTube video IDs from URLs
"""

import re
from typing import Optional
from urllib.parse import urlparse, parse_qs
import logging

logger = logging.getLogger(__name__)

class URLExtractor:
    """Service for extracting YouTube video IDs from various URL formats"""
    
    def __init__(self):
        # Patterns for different YouTube URL formats
        self.url_patterns = [
            # Standard YouTube URLs
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
            # Short YouTube URLs
            r'(?:https?://)?youtu\.be/([a-zA-Z0-9_-]{11})',
            # YouTube embed URLs
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})',
            # YouTube shorts URLs
            r'(?:https?://)?(?:www\.)?youtube\.com/shorts/([a-zA-Z0-9_-]{11})',
            # YouTube live URLs
            r'(?:https?://)?(?:www\.)?youtube\.com/live/([a-zA-Z0-9_-]{11})',
            # Mobile YouTube URLs
            r'(?:https?://)?m\.youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
            # Just video ID pattern
            r'^([a-zA-Z0-9_-]{11})$'
        ]
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """
        Extract YouTube video ID from various URL formats
        
        Args:
            url: YouTube URL or video ID
            
        Returns:
            Video ID string or None if not found
        """
        if not url:
            return None
        
        # Clean the URL
        url = url.strip()
        
        # Try pattern matching first
        video_id = self._extract_with_patterns(url)
        if video_id:
            return video_id
        
        # Try URL parsing as fallback
        video_id = self._extract_with_urlparse(url)
        if video_id:
            return video_id
        
        logger.warning(f"Could not extract video ID from URL: {url}")
        return None
    
    def _extract_with_patterns(self, url: str) -> Optional[str]:
        """Extract video ID using regex patterns"""
        for pattern in self.url_patterns:
            match = re.search(pattern, url, re.IGNORECASE)
            if match:
                video_id = match.group(1)
                if self._is_valid_video_id(video_id):
                    return video_id
        return None
    
    def _extract_with_urlparse(self, url: str) -> Optional[str]:
        """Extract video ID using URL parsing"""
        try:
            # Add protocol if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            parsed_url = urlparse(url)
            
            # Handle different YouTube domains
            if parsed_url.hostname in ['www.youtube.com', 'youtube.com', 'm.youtube.com']:
                # Standard YouTube URL
                if parsed_url.path == '/watch':
                    query_params = parse_qs(parsed_url.query)
                    video_id = query_params.get('v', [None])[0]
                    if video_id and self._is_valid_video_id(video_id):
                        return video_id
                
                # Embed URL
                elif parsed_url.path.startswith('/embed/'):
                    video_id = parsed_url.path.split('/embed/')[1].split('?')[0]
                    if self._is_valid_video_id(video_id):
                        return video_id
                
                # Shorts URL
                elif parsed_url.path.startswith('/shorts/'):
                    video_id = parsed_url.path.split('/shorts/')[1].split('?')[0]
                    if self._is_valid_video_id(video_id):
                        return video_id
                
                # Live URL
                elif parsed_url.path.startswith('/live/'):
                    video_id = parsed_url.path.split('/live/')[1].split('?')[0]
                    if self._is_valid_video_id(video_id):
                        return video_id
            
            # Handle youtu.be short URLs
            elif parsed_url.hostname == 'youtu.be':
                video_id = parsed_url.path[1:]  # Remove leading slash
                if self._is_valid_video_id(video_id):
                    return video_id
            
        except Exception as e:
            logger.error(f"Error parsing URL {url}: {str(e)}")
        
        return None
    
    def _is_valid_video_id(self, video_id: str) -> bool:
        """
        Validate YouTube video ID format
        
        Args:
            video_id: Video ID to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not video_id:
            return False
        
        # YouTube video IDs are 11 characters long and contain alphanumeric characters, hyphens, and underscores
        return bool(re.match(r'^[a-zA-Z0-9_-]{11}$', video_id))
    
    def is_youtube_url(self, url: str) -> bool:
        """
        Check if URL is a YouTube URL
        
        Args:
            url: URL to check
            
        Returns:
            True if YouTube URL, False otherwise
        """
        if not url:
            return False
        
        youtube_domains = [
            'youtube.com',
            'www.youtube.com',
            'm.youtube.com',
            'youtu.be'
        ]
        
        try:
            # Add protocol if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            parsed_url = urlparse(url)
            return parsed_url.hostname in youtube_domains
            
        except Exception:
            return False
    
    def get_video_url(self, video_id: str) -> str:
        """
        Convert video ID to standard YouTube URL
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Standard YouTube URL
        """
        if not self._is_valid_video_id(video_id):
            raise ValueError("Invalid video ID")
        
        return f"https://www.youtube.com/watch?v={video_id}"