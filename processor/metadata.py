"""
Metadata processor untuk extract dan embed metadata
"""
from pathlib import Path
from typing import Dict, Optional
from utils.logger import logger


class MetadataProcessor:
    """Extract dan embed metadata ke audio files"""
    
    @staticmethod
    def extract_metadata(file_path: Path) -> Dict[str, str]:
        """
        Extract metadata dari audio file
        
        Args:
            file_path: Path ke audio file
        
        Returns:
            Dictionary dengan metadata
        """
        try:
            from mutagen import File
            
            audio = File(str(file_path), easy=True)
            
            if audio is None:
                return {
                    'title': file_path.stem,
                    'artist': 'Unknown Artist',
                    'album': 'Unknown Album',
                }
            
            return {
                'title': audio.get('title', [file_path.stem])[0],
                'artist': audio.get('artist', ['Unknown Artist'])[0],
                'album': audio.get('album', ['Unknown Album'])[0],
                'date': audio.get('date', [''])[0],
                'genre': audio.get('genre', [''])[0],
            }
        
        except Exception as e:
            logger.warning(f"Could not extract metadata: {e}")
            return {
                'title': file_path.stem,
                'artist': 'Unknown Artist',
                'album': 'Unknown Album',
            }
    
    @staticmethod
    def embed_metadata(file_path: Path, metadata: Dict[str, str]) -> bool:
        """
        Embed metadata ke audio file
        
        Args:
            file_path: Path ke audio file
            metadata: Dictionary dengan metadata
        
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            from mutagen import File
            
            audio = File(str(file_path), easy=True)
            
            if audio is None:
                logger.warning(f"Could not open file for metadata embedding: {file_path}")
                return False
            
            if 'title' in metadata and metadata['title']:
                audio['title'] = metadata['title']
            if 'artist' in metadata and metadata['artist']:
                audio['artist'] = metadata['artist']
            if 'album' in metadata and metadata['album']:
                audio['album'] = metadata['album']
            if 'date' in metadata and metadata['date']:
                audio['date'] = metadata['date']
            if 'genre' in metadata and metadata['genre']:
                audio['genre'] = metadata['genre']
            
            audio.save()
            logger.debug(f"Metadata embedded: {file_path.name}")
            return True
        
        except Exception as e:
            logger.warning(f"Error embedding metadata: {e}")
            return False
