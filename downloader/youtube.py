"""
YouTube downloader menggunakan yt-dlp
"""
from pathlib import Path
from typing import List, Optional
from utils.logger import logger
import yt_dlp


class YouTubeDownloader:
    """Downloader untuk YouTube videos dan playlists"""
    
    @staticmethod
    def check_ytdlp() -> bool:
        """Check apakah yt-dlp terinstall"""
        try:
            import yt_dlp
            return True
        except ImportError:
            return False
    
    @staticmethod
    def download_video(
        url: str,
        output_dir: Path,
        audio_format: str = 'mp3',
        audio_quality: int = 320
    ) -> Optional[Path]:
        """Download single YouTube video"""
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(output_dir / '%(title)s.%(ext)s'),
                'writethumbnail': True,
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': audio_format.lower(),
                        'preferredquality': str(audio_quality),
                    },
                    {
                        'key': 'FFmpegMetadata',
                        'add_metadata': True,
                    },
                    {
                        'key': 'EmbedThumbnail',
                    },
                ],
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if not info:
                    return None

                # filename returned from prepare_filename uses original extension, but FFmpegExtractAudio changes it to audio_format.
                base_filename = ydl.prepare_filename(info)
                final_filename = Path(base_filename).with_suffix(f'.{audio_format.lower()}')

                if final_filename.exists():
                    return final_filename

                # fallback just in case
                for file in output_dir.glob(f'*.{audio_format.lower()}'):
                    return file

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
            output_dir.mkdir(parents=True, exist_ok=True)
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(output_dir / '%(title)s.%(ext)s'),
                'writethumbnail': True,
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': audio_format.lower(),
                        'preferredquality': str(audio_quality),
                    },
                    {
                        'key': 'FFmpegMetadata',
                        'add_metadata': True,
                    },
                    {
                        'key': 'EmbedThumbnail',
                    },
                ],
                'quiet': True,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            files = list(output_dir.glob(f'*.{audio_format.lower()}'))
            return files
            
        except Exception as e:
            logger.error(f"Error downloading YouTube playlist: {e}")
            return []
