"""
Platform detector - mengidentifikasi URL adalah dari Spotify, YouTube, atau platform lain
"""
import re
from typing import Optional, Tuple
from enum import Enum
from utils.logger import logger


class Platform(Enum):
    """Enum untuk platform yang didukung"""
    SPOTIFY = "spotify"
    YOUTUBE = "youtube"
    UNKNOWN = "unknown"


class URLDetector:
    """Deteksi platform dari URL"""
    
    # Pattern untuk berbagai platform
    PATTERNS = {
        Platform.SPOTIFY: [
            r'spotify\.com/(track|album|playlist)/[\w\d]+',
            r'open\.spotify\.com/(track|album|playlist)/[\w\d]+'
        ],
        Platform.YOUTUBE: [
            r'youtube\.com/(watch\?v=|playlist\?list=)',
            r'youtu\.be/[\w\d-]+',
            r'youtube\.com/watch\?.*v=[\w\d-]+'
        ]
    }
    
    @staticmethod
    def detect(url: str) -> Tuple[Platform, Optional[str]]:
        """
        Deteksi platform dari URL
        
        Args:
            url: URL yang akan dideteksi
        
        Returns:
            Tuple (Platform, content_type) - content_type adalah 'track', 'album', 'playlist', dll
        """
        url = url.strip()
        
        # Check Spotify
        if 'spotify' in url:
            content_type = URLDetector._get_spotify_content_type(url)
            logger.debug(f"Detected Spotify URL: {content_type}")
            return Platform.SPOTIFY, content_type
        
        # Check YouTube
        elif 'youtube' in url or 'youtu.be' in url:
            content_type = URLDetector._get_youtube_content_type(url)
            logger.debug(f"Detected YouTube URL: {content_type}")
            return Platform.YOUTUBE, content_type
        
        else:
            logger.warning(f"Unknown platform for URL: {url}")
            return Platform.UNKNOWN, None
    
    @staticmethod
    def _get_spotify_content_type(url: str) -> str:
        """Identifikasi tipe content Spotify (track/album/playlist)"""
        if '/track/' in url:
            return 'track'
        elif '/album/' in url:
            return 'album'
        elif '/playlist/' in url:
            return 'playlist'
        else:
            return 'unknown'
    
    @staticmethod
    def _get_youtube_content_type(url: str) -> str:
        """Identifikasi tipe content YouTube (video/playlist)"""
        if 'playlist' in url or 'list=' in url:
            return 'playlist'
        else:
            return 'video'
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """
        Validasi apakah URL adalah valid URL dari platform yang didukung
        
        Args:
            url: URL yang akan divalidasi
        
        Returns:
            True jika valid, False jika tidak
        """
        url = url.strip()
        
        for platform, patterns in URLDetector.PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, url, re.IGNORECASE):
                    return True
        
        return False
