"""
Audio converter menggunakan FFmpeg
"""
from pathlib import Path
from typing import Optional
from utils.logger import logger


class AudioConverter:
    """Convert audio files ke format berbeda"""
    
    @staticmethod
    def check_ffmpeg() -> bool:
        """Check apakah FFmpeg terinstall"""
        try:
            import subprocess
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    @staticmethod
    def convert_to_mp3(
        input_file: Path,
        output_file: Path,
        bitrate: int = 320
    ) -> bool:
        """
        Convert audio ke MP3
        
        Args:
            input_file: Path ke input file
            output_file: Path ke output file
            bitrate: Bitrate dalam kbps
        
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            import subprocess
            
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            cmd = [
                'ffmpeg',
                '-i', str(input_file),
                '-b:a', f'{bitrate}k',
                '-y',
                str(output_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True)
            
            if result.returncode == 0:
                logger.debug(f"Converted to MP3: {output_file.name}")
                return True
            else:
                logger.error("FFmpeg conversion to MP3 failed")
                return False
        
        except Exception as e:
            logger.error(f"Error converting to MP3: {e}")
            return False
    
    @staticmethod
    def convert_to_flac(
        input_file: Path,
        output_file: Path
    ) -> bool:
        """
        Convert audio ke FLAC
        
        Args:
            input_file: Path ke input file
            output_file: Path ke output file
        
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            import subprocess
            
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            cmd = [
                'ffmpeg',
                '-i', str(input_file),
                '-y',
                str(output_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True)
            
            if result.returncode == 0:
                logger.debug(f"Converted to FLAC: {output_file.name}")
                return True
            else:
                logger.error("FFmpeg conversion to FLAC failed")
                return False
        
        except Exception as e:
            logger.error(f"Error converting to FLAC: {e}")
            return False
