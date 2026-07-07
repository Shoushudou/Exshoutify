"""
YouTube downloader menggunakan yt-dlp
"""
from pathlib import Path
from typing import List, Optional
from utils.logger import logger


class YouTubeDownloader:
    """Downloader untuk YouTube videos dan playlists"""
    
    @staticmethod
    def check_ytdlp() -> bool:
        """Check apakah yt-dlp terinstall"""
        try:
            import subprocess
            result = subprocess.run(['yt-dlp', '--version'], capture_output=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    @staticmethod
    def download_video(
        url: str,
        output_path: Path,
        audio_format: str = 'mp3',
        audio_quality: int = 320
    ) -> Optional[Path]:
        """Download single YouTube video"""
        try:
            import subprocess
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            cmd = [
                'yt-dlp',
                '-x',
                '--audio-format', audio_format.lower(),
                '--audio-quality', f'{audio_quality}K',
                '--add-metadata',
                '--embed-thumbnail',
                '-o', str(output_path.with_suffix('')),
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Find downloaded file
                for file in output_path.parent.glob(f'*{output_path.stem}*'):
                    if file.suffix.lower() == f'.{audio_format.lower()}':
                        return file
            else:
                logger.error(f"yt-dlp error: {result.stderr}")
                return None
        
        except Exception as e:
            logger.error(f"Error downloading YouTube video: {e}")
            return None
    
    @staticmethod
    def download_playlist(
        url: str,
        output_dir: Path,
        audio_format: str = 'mp3',
        audio_quality: int = 320
    ) -> List[Path]:
        """Download YouTube playlist"""
        try:
            import subprocess
            
            output_dir.mkdir(parents=True, exist_ok=True)
            
            cmd = [
                'yt-dlp',
                '-x',
                '--audio-format', audio_format.lower(),
                '--audio-quality', f'{audio_quality}K',
                '--add-metadata',
                '--embed-thumbnail',
                '-o', str(output_dir / '%(title)s'),
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                files = list(output_dir.glob(f'*.{audio_format.lower()}'))
                return files
            else:
                logger.error(f"yt-dlp error: {result.stderr}")
                return []
        
        except Exception as e:
            logger.error(f"Error downloading YouTube playlist: {e}")
            return []
