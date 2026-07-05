"""
Cover processor untuk download dan embed album cover
"""
from pathlib import Path
from typing import Optional
from utils.logger import logger


class CoverProcessor:
    """Download dan embed album cover"""
    
    @staticmethod
    def download_cover(url: str, output_path: Path) -> bool:
        """
        Download cover dari URL
        
        Args:
            url: URL ke cover image
            output_path: Path untuk save cover
        
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            import requests
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                logger.debug(f"Cover downloaded: {output_path}")
                return True
            else:
                logger.warning(f"Failed to download cover: HTTP {response.status_code}")
                return False
        
        except Exception as e:
            logger.warning(f"Error downloading cover: {e}")
            return False
    
    @staticmethod
    def embed_cover(audio_file: Path, cover_path: Path) -> bool:
        """
        Embed cover ke audio file
        
        Args:
            audio_file: Path ke audio file
            cover_path: Path ke cover image
        
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            from mutagen.id3 import ID3, APIC
            from PIL import Image
            
            if not cover_path.exists():
                logger.warning(f"Cover file not found: {cover_path}")
                return False
            
            # Verify it's a valid image
            try:
                Image.open(cover_path)
            except Exception:
                logger.warning(f"Invalid image file: {cover_path}")
                return False
            
            # Add cover to ID3 (for MP3)
            if audio_file.suffix.lower() == '.mp3':
                audio = ID3(str(audio_file))
                with open(cover_path, 'rb') as f:
                    audio.add(APIC(
                        encoding=3,
                        mime='image/jpeg',
                        type=3,
                        desc='',
                        data=f.read()
                    ))
                audio.save()
                logger.debug(f"Cover embedded: {audio_file.name}")
                return True
            else:
                logger.warning(f"Cover embedding not supported for {audio_file.suffix}")
                return False
        
        except Exception as e:
            logger.warning(f"Error embedding cover: {e}")
            return False
