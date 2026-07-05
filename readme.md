# 🎵 Music Downloader untuk Termux

Aplikasi downloader musik yang powerful, lengkap, dan production-ready untuk Spotify & YouTube. Dapat berjalan di Termux (Linux Android) dan sistem Linux/macOS lainnya.

## ✨ Features

- ✅ **Dual Platform Support**: Spotify & YouTube
- ✅ **Multiple Content Types**: Track, Album, Playlist
- ✅ **Audio Quality**: 320kbps MP3 atau FLAC lossless
- ✅ **Complete Metadata**: Title, Artist, Album, Year, Genre
- ✅ **Album Cover**: Auto-download & embed cover art
- ✅ **Smart Naming**: Auto-sanitize filename
- ✅ **Batch Download**: Download multiple URLs
- ✅ **Parallel Download**: Multi-threading support
- ✅ **Organized Structure**: Artist/Album folder structure
- ✅ **Progress Logging**: Real-time download status
- ✅ **Error Handling**: Auto-retry on failures
- ✅ **FFmpeg Integration**: Convert & embed metadata

## 📋 Requirements

### System Requirements
- Python 3.8+
- FFmpeg (untuk audio processing)
- Internet connection

### Supported Platforms
- Termux (Android)
- Ubuntu/Debian
- macOS
- CentOS/RHEL

## 🚀 Installation

### Termux (Recommended)

```bash
# Clone repository
cd ~/storage/downloads
git clone https://github.com/shouShudou/exshoutify.git
cd exshoutify

# Run installation script
bash install.sh
```

### Manual Installation

```bash
# Install system dependencies
# Ubuntu/Debian
sudo apt install python3 python3-pip ffmpeg

# Termux
pkg install python pip ffmpeg

# Install Python packages
pip install -r requirements.txt
```

## 📖 Usage

### Basic Usage

```bash
# Download single Spotify track
exshoutify "https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp"

# Download YouTube video
exshoutify "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Download Spotify album
exshoutify "https://open.spotify.com/album/3T4tUhGYeRz9D2ObvXZnVJ"

# Download YouTube playlist
exshoutify "https://www.youtube.com/playlist?list=PLx"
```

### Advanced Options

```bash
# Download with FLAC format (lossless)
exshoutify "url" --format flac

# Download dengan kualitas lebih rendah
exshoutify "url" --quality 192

# Organize downloads ke Artist/Album folder
exshoutify "url" --organize

# Batch download dari file
exshoutify --batch urls.txt

# Parallel download (lebih cepat)
exshoutify --batch urls.txt --parallel

# Combine options
exshoutify --batch urls.txt --organize --format flac --parallel --quality 320
```

## 📁 Project Structure

```
music-downloader-termux/
├── main.py                 # Entry point CLI
├── detector.py             # URL platform detection
├── requirements.txt        # Python dependencies
├── install.sh             # Installation script
├── README.md              # Documentation
├── downloader/
│   ├── __init__.py
│   ├── spotify.py         # Spotify downloader
│   └── youtube.py         # YouTube downloader
├── processor/
│   ├── __init__.py
│   ├── metadata.py        # Metadata handling
│   ├── cover.py          # Album cover processing
│   └── converter.py       # Audio conversion
└── utils/
    ├── __init__.py
    ├── logger.py          # Logging utility
    ├── sanitizer.py       # Filename sanitizer
    └── config.py          # Configuration
```

## ⚙️ Configuration

Edit `utils/config.py` untuk customize:

```python
# Download directory
DOWNLOAD_DIR = Path.home() / "Music" / "Downloads"

# Audio quality
AUDIO_QUALITY = {
    "mp3": {"default": 320, "options": [128, 192, 256, 320]},
    "flac": {"default": "best", "lossless": True}
}

# Batch processing
BATCH_CONFIG = {
    "max_workers": 3,
    "queue_mode": True,
    "timeout_per_track": 300
}
```

## 🎯 Examples

### Download Single Track
```bash
exshoutify "https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp" --organize
```

### Create Batch File (urls.txt)
```
https://open.spotify.com/track/xxx
https://www.youtube.com/watch?v=yyy
https://open.spotify.com/album/zzz
```

### Download Batch
```bash
exshoutify --batch urls.txt --organize --parallel --quality 320
```

### Download Playlist
```bash
exshoutify "https://open.spotify.com/playlist/xxx" --organize --format flac
```

## 📊 Download Locations

Default save locations:

```
~/Music/Downloads/          # Flat structure
~/Music/Organized/          # Organized by Artist/Album
~/.music_downloader/logs/   # Logs
~/.music_downloader/temp/   # Temporary files
```

## 🔧 Troubleshooting

### FFmpeg not found
```bash
# Termux
pkg install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

### spotdl not working
```bash
pip install --upgrade spotdl
```

### yt-dlp not working
```bash
pip install --upgrade yt-dlp
```

### Permission denied in Termux
```bash
chmod +x install.sh
bash install.sh
```

### Out of storage
Clean temporary files:
```bash
rm -rf ~/.exhsoutify/temp/*
```

## 📝 Logging

Logs disimpan di: `~/.exshoutify/logs/`

Format:
```
[INFO] Downloading Spotify track: ...
[DEBUG] Converting to MP3 320kbps: ...
[ERROR] Error downloading: ...
