"""
Spotify downloader menggunakan spotdl
"""
from pathlib import Path
from typing import List, Optional
from utils.logger import logger


class SpotifyDownloader:
    """Downloader untuk Spotify tracks, albums, playlists"""
    
    @staticmethod
    def check_spotdl() -> bool:
        """Check apakah spotdl terinstall"""
        try:
            import subprocess
            result = subprocess.run(['spotdl', '--version'], capture_output=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    @staticmethod
    def download_track(
        url: str,
        output_dir: Path,
        audio_format: str = 'mp3',
        audio_quality: int = 320
    ) -> Optional[Path]:
        """Download single Spotify track"""
        try:
            import subprocess
            
            output_dir.mkdir(parents=True, exist_ok=True)
            
            cmd = [
                'spotdl',
                'download',
                url,
                '--output',
                str(output_dir),
                '--format',
                audio_format.lower()
            ]
            
            if audio_format.lower() == 'mp3':
                cmd.extend(['--bitrate', f'{audio_quality}k'])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Find downloaded file
                for file in output_dir.glob(f'*.{audio_format.lower()}'):
                    return file
            else:
                logger.error(f"spotdl error: {result.stderr}")
                return None
        
        except Exception as e:
            logger.error(f"Error downloading Spotify track: {e}")
            return None
    
    @staticmethod
    def download_album(
        url: str,
        output_dir: Path,
        audio_format: str = 'mp3',
        audio_quality: int = 320
    ) -> List[Path]:
        """Download Spotify album"""
        try:
            import subprocess
            
            output_dir.mkdir(parents=True, exist_ok=True)
            
            cmd = [
                'spotdl',
                'download',
                url,
                '--output',
                str(output_dir),
                '--format',
                audio_format.lower()
            ]
            
            if audio_format.lower() == 'mp3':
                cmd.extend(['--bitrate', f'{audio_quality}k'])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                files = list(output_dir.glob(f'*.{audio_format.lower()}'))
                return files
            else:
                logger.error(f"spotdl error: {result.stderr}")
                return []
        
        except Exception as e:
            logger.error(f"Error downloading Spotify album: {e}")
            return []
    
    @staticmethod
    def download_playlist(
        url: str,
        output_dir: Path,
        audio_format: str = 'mp3',
        audio_quality: int = 320
    ) -> List[Path]:
        """Download Spotify playlist"""
        try:
            import subprocess
            
            output_dir.mkdir(parents=True, exist_ok=True)
            
            cmd = [
                'spotdl',
                'download',
                url,
                '--output',
                str(output_dir),
                '--format',
                audio_format.lower()
            ]
            
            if audio_format.lower() == 'mp3':
                cmd.extend(['--bitrate', f'{audio_quality}k'])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                files = list(output_dir.glob(f'*.{audio_format.lower()}'))
                return files
            else:
                logger.error(f"spotdl error: {result.stderr}")
                return []
        
        except Exception as e:
            logger.error(f"Error downloading Spotify playlist: {e}")
            return []
