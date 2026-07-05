"""
Configuration constants untuk aplikasi
"""
from pathlib import Path

# Download directories
DOWNLOAD_DIR = Path.home() / "Music" / "Downloads"
ORGANIZED_DOWNLOAD_DIR = Path.home() / "Music" / "Organized"

# Ensure directories exist
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
ORGANIZED_DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Audio quality settings
AUDIO_QUALITY = {
    "mp3": {"default": 320, "options": [128, 192, 256, 320]},
    "flac": {"default": "best", "lossless": True}
}

# Batch processing config
BATCH_CONFIG = {
    "max_workers": 3,
    "queue_mode": True,
    "timeout_per_track": 300  # 5 minutes
}

# Temporary directories
TEMP_DIR = Path.home() / ".exshoutify" / "temp"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# Logs directory
LOGS_DIR = Path.home() / ".exshoutify" / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
