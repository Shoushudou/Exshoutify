"""
Music Downloader Termux - Main CLI Application
Aplikasi lengkap untuk download musik dari Spotify dan YouTube
"""
import sys
import shutil
import argparse
from pathlib import Path
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from detector import URLDetector, Platform
from downloader.spotify import SpotifyDownloader
from downloader.youtube import YouTubeDownloader
from processor.metadata import MetadataProcessor
from processor.converter import AudioConverter
from utils.logger import logger
from utils.sanitizer import sanitize_filename, sanitize_path_part
from utils.config import DOWNLOAD_DIR, ORGANIZED_DOWNLOAD_DIR, BATCH_CONFIG, AUDIO_QUALITY


class MusicDownloader:
    """Main application class untuk download musik"""
    
    def __init__(self, quality: int = 320, audio_format: str = 'mp3', organize: bool = False, output_dir: Optional[Path] = None):
        """
        Initialize Music Downloader
        
        Args:
            quality: Audio quality dalam kbps (default: 320)
            audio_format: Audio format (mp3/flac, default: mp3)
            organize: Organize downloads ke folder Artist/Album (default: False)
            output_dir: Custom output directory (optional)
        """
        self.quality = quality
        self.audio_format = audio_format
        self.organize = organize
        
        # Set output directory
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = ORGANIZED_DOWNLOAD_DIR if organize else DOWNLOAD_DIR
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Check dependencies
        self._check_dependencies()
    
    def _check_dependencies(self):
        """Check semua dependencies yang diperlukan"""
        logger.info("Checking dependencies...")
        
        # Check FFmpeg
        if not AudioConverter.check_ffmpeg():
            logger.error("FFmpeg is required but not found")
            logger.info("Install FFmpeg:")
            logger.info("  Ubuntu/Debian: sudo apt install ffmpeg")
            logger.info("  Termux: pkg install ffmpeg")
            sys.exit(1)
        
        # Check spotdl
        if not SpotifyDownloader.check_spotdl():
            logger.warning("spotdl not found - Spotify download will not work")
        
        # Check yt-dlp
        if not YouTubeDownloader.check_ytdlp():
            logger.warning("yt-dlp not found - YouTube download will not work")
        
        logger.info("Dependencies check completed")
    
    def download_single(self, url: str) -> Optional[Path]:
        """
        Download single track/video
        
        Args:
            url: URL ke track/video yang akan di-download
        
        Returns:
            Path ke downloaded file atau None jika gagal
        """
        logger.info(f"Processing: {url}")
        
        # Detect platform
        platform, content_type = URLDetector.detect(url)
        
        if platform == Platform.UNKNOWN:
            logger.error(f"Unsupported URL: {url}")
            return None
        
        try:
            if platform == Platform.SPOTIFY:
                return self._download_spotify(url, content_type)
            elif platform == Platform.YOUTUBE:
                return self._download_youtube(url, content_type)
        
        except Exception as e:
            logger.error(f"Error downloading {url}: {e}")
            return None
    
    def _download_spotify(self, url: str, content_type: str) -> Optional[Path]:
        """Download dari Spotify"""
        logger.debug(f"Downloading from Spotify - Type: {content_type}")
        
        temp_dir = self.output_dir / ".temp_spotify"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            if content_type == 'track':
                downloaded_file = SpotifyDownloader.download_track(
                    url, temp_dir,
                    audio_format=self.audio_format,
                    audio_quality=self.quality
                )
                return self._process_downloaded_file(downloaded_file)
            
            elif content_type == 'album':
                downloaded_files = SpotifyDownloader.download_album(
                    url, temp_dir,
                    audio_format=self.audio_format,
                    audio_quality=self.quality
                )
                # FIX: Return all results, not just first one
                results = [self._process_downloaded_file(f) for f in downloaded_files]
                return results
            
            elif content_type == 'playlist':
                downloaded_files = SpotifyDownloader.download_playlist(
                    url, temp_dir,
                    audio_format=self.audio_format,
                    audio_quality=self.quality
                )
                # FIX: Return all results, not just first one
                results = [self._process_downloaded_file(f) for f in downloaded_files]
                return results
        
        except Exception as e:
            logger.error(f"Spotify download error: {e}")
            return None
    
    def _download_youtube(self, url: str, content_type: str) -> Optional[Path]:
        """Download dari YouTube"""
        logger.debug(f"Downloading from YouTube - Type: {content_type}")
        
        temp_dir = self.output_dir / ".temp_youtube"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            if content_type == 'video':
                downloaded_file = YouTubeDownloader.download_video(
                    url, temp_dir,
                    audio_format=self.audio_format,
                    audio_quality=self.quality
                )
                return self._process_downloaded_file(downloaded_file)
            
            elif content_type == 'playlist':
                downloaded_files = YouTubeDownloader.download_playlist(
                    url, temp_dir,
                    audio_format=self.audio_format,
                    audio_quality=self.quality
                )
                # FIX: Return all results, not just first one
                results = [self._process_downloaded_file(f) for f in downloaded_files]
                return results
        
        except Exception as e:
            logger.error(f"YouTube download error: {e}")
            return None
    
    def _process_downloaded_file(self, file_path: Optional[Path]) -> Optional[Path]:
        """
        Process downloaded file - move to organized folder and embed extra metadata if needed
        
        Args:
            file_path: Path ke downloaded file
        
        Returns:
            Path ke processed file atau None jika gagal
        """
        if not file_path or not file_path.exists():
            logger.error("Downloaded file not found")
            return None
        
        try:
            logger.info(f"Processing: {file_path.name}")
            
            # Extract metadata
            metadata = MetadataProcessor.extract_metadata(file_path)
            
            # Create organized path jika perlu
            if self.organize:
                artist = sanitize_path_part(metadata.get('artist', 'Unknown Artist'))
                album = sanitize_path_part(metadata.get('album', 'Unknown Album'))
                title = sanitize_filename(metadata.get('title', file_path.stem))
                
                output_path = self.output_dir / artist / album / f"{title}.{self.audio_format}"
                output_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                # Simple flat structure
                title = sanitize_filename(metadata.get('title', file_path.stem))
                output_path = self.output_dir / f"{title}.{self.audio_format}"
            
            # FIX: Use shutil.move() for cross-disk safety
            output_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file_path), str(output_path))
            
            # Embed metadata (optional, just to be sure extra fields are there if available)
            # Cover art is not stripped by mutagen `easy=True`.
            MetadataProcessor.embed_metadata(output_path, metadata)
            
            logger.info(f"✓ Successfully saved: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            return None
    
    def download_batch(self, urls: List[str], parallel: bool = False) -> List[Path]:
        """
        Download multiple URLs
        
        Args:
            urls: List of URLs
            parallel: Use multi-threading (default: False)
        
        Returns:
            List of successfully downloaded files
        """
        logger.info(f"Starting batch download: {len(urls)} items")
        
        successful = []
        
        if parallel:
            # Parallel download dengan ThreadPoolExecutor
            max_workers = BATCH_CONFIG.get('max_workers', 3)
            logger.info(f"Using {max_workers} workers for parallel download")
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_url = {
                    executor.submit(self.download_single, url): url
                    for url in urls
                }
                
                for future in as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        result = future.result()
                        if result:
                            # Handle both single file and list of files
                            if isinstance(result, list):
                                successful.extend([r for r in result if r])
                            else:
                                successful.append(result)
                    except Exception as e:
                        logger.error(f"Error downloading {url}: {e}")
        else:
            # Sequential download
            for i, url in enumerate(urls, 1):
                logger.info(f"[{i}/{len(urls)}] Downloading...")
                result = self.download_single(url)
                if result:
                    # Handle both single file and list of files
                    if isinstance(result, list):
                        successful.extend([r for r in result if r])
                    else:
                        successful.append(result)
        
        logger.info(f"Batch download completed: {len(successful)}/{len(urls)} successful")
        return successful


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Music Downloader untuk Spotify & YouTube',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download single Spotify track
  python3 main.py "https://open.spotify.com/track/..."
  
  # Download YouTube video
  python3 main.py "https://www.youtube.com/watch?v=..."
  
  # Download album
  python3 main.py "https://open.spotify.com/album/..."
  
  # Download with FLAC format
  python3 main.py "url" --format flac
  
  # Download multiple URLs from file
  python3 main.py --batch urls.txt
  
  # Organized folder structure
  python3 main.py "url" --organize
  
  # Parallel download
  python3 main.py --batch urls.txt --parallel
  
  # Custom output directory
  python3 main.py "url" --output /path/to/directory
        """
    )
    
    parser.add_argument(
        'url',
        nargs='?',
        help='URL ke track/album/playlist'
    )
    parser.add_argument(
        '--batch',
        type=str,
        help='File berisi daftar URLs (satu per baris)'
    )
    parser.add_argument(
        '--quality',
        type=int,
        default=320,
        choices=[128, 192, 256, 320],
        help='Audio quality dalam kbps (default: 320)'
    )
    parser.add_argument(
        '--format',
        type=str,
        default='mp3',
        choices=['mp3', 'flac'],
        help='Audio format (default: mp3)'
    )
    parser.add_argument(
        '--organize',
        action='store_true',
        help='Organize downloads ke folder Artist/Album/Track'
    )
    parser.add_argument(
        '--parallel',
        action='store_true',
        help='Use parallel download untuk batch (default: sequential)'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Custom output directory'
    )
    
    args = parser.parse_args()
    
    # Validasi arguments
    if not args.url and not args.batch:
        parser.print_help()
        return
    
    # Initialize downloader
    downloader = MusicDownloader(
        quality=args.quality,
        audio_format=args.format,
        organize=args.organize,
        output_dir=Path(args.output) if args.output else None  # FIX: Use output_dir parameter
    )
    
    try:
        # Single download
        if args.url:
            result = downloader.download_single(args.url)  # FIX: Capture result
            if result:
                if isinstance(result, list):
                    logger.info(f"✓ Downloaded {len(result)} file(s)")
                else:
                    logger.info(f"✓ Download successful: {result}")
            else:
                logger.error("Download failed")
                sys.exit(1)
        
        # Batch download
        elif args.batch:
            batch_file = Path(args.batch)
            if not batch_file.exists():
                logger.error(f"Batch file not found: {args.batch}")
                return
            
            with open(batch_file, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
            
            if not urls:
                logger.error("No URLs found in batch file")
                return
            
            results = downloader.download_batch(urls, parallel=args.parallel)
            if results:
                logger.info(f"✓ Successfully downloaded {len(results)} file(s)")
            else:
                logger.error("No files were downloaded")
                sys.exit(1)
    
    except KeyboardInterrupt:
        logger.warning("\nDownload cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
