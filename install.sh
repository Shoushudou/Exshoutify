#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║      Music Downloader untuk Termux - Installation (Fixed)      ║"
echo "╚════════════════════════════════════════════════════════════════╝"

# Update packages
echo "[*] Updating package manager..."
pkg update -y
pkg upgrade -y

# Install dependencies
echo "[*] Installing system dependencies..."
pkg install -y \
    python \
    python-pip \
    ffmpeg \
    git \
    curl \
    build-essential

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "[✓] Python version: $python_version"

# Check FFmpeg
if command -v ffmpeg &> /dev/null; then
    ffmpeg_version=$(ffmpeg -version 2>/dev/null | head -1)
    echo "[✓] FFmpeg installed: $ffmpeg_version"
else
    echo "[✗] FFmpeg not found - installation may have failed"
    exit 1
fi

# Upgrade pip safely
echo "[*] Upgrading pip..."
python3 -m pip install --upgrade pip --break-system-packages 2>/dev/null || true

# Install Python dependencies dengan break-system-packages
echo "[*] Installing Python packages..."
python3 -m pip install \
    --break-system-packages \
    --no-cache-dir \
    spotdl==4.3.1 \
    yt-dlp \
    mutagen \
    pillow \
    requests \
    colorama \
    tqdm \
    python-dotenv

# Check installations
echo ""
echo "[*] Verifying installations..."

python3 -c "import spotdl; print('[✓] spotdl installed')" 2>/dev/null || echo "[✗] spotdl installation failed"
python3 -c "import yt_dlp; print('[✓] yt-dlp installed')" 2>/dev/null || echo "[⚠] yt-dlp warning"
python3 -c "import mutagen; print('[✓] mutagen installed')" 2>/dev/null || echo "[⚠] mutagen warning"
python3 -c "import PIL; print('[✓] pillow installed')" 2>/dev/null || echo "[⚠] pillow warning"
python3 -c "import requests; print('[✓] requests installed')" 2>/dev/null || echo "[⚠] requests warning"
python3 -c "import colorama; print('[✓] colorama installed')" 2>/dev/null || echo "[⚠] colorama warning"
python3 -c "import tqdm; print('[✓] tqdm installed')" 2>/dev/null || echo "[⚠] tqdm warning"

# Create necessary directories
echo "[*] Creating directories..."
mkdir -p ~/Music/Downloads
mkdir -p ~/Music/Organized
mkdir -p ~/.music_downloader/logs
mkdir -p ~/.music_downloader/temp

# Install exshoutify command
echo "[*] Installing exshoutify command..."
if [ -n "$PREFIX" ]; then
    # Termux
    BIN_DIR="$PREFIX/bin"
else
    # Standard Linux
    BIN_DIR="/usr/local/bin"
fi

if [ -w "$BIN_DIR" ] || [ -n "$PREFIX" ]; then
    cat << EOF > "$BIN_DIR/exshoutify"
#!/bin/bash
PROJECT_DIR="$(pwd)"
python3 "\$PROJECT_DIR/main.py" "\$@"
EOF
    chmod +x "$BIN_DIR/exshoutify"
    echo "[✓] Installed to $BIN_DIR/exshoutify"
else
    echo "[!] Requires sudo to install command to $BIN_DIR"
    cat << EOF | sudo tee "$BIN_DIR/exshoutify" > /dev/null
#!/bin/bash
PROJECT_DIR="$(pwd)"
python3 "\$PROJECT_DIR/main.py" "\$@"
EOF
    sudo chmod +x "$BIN_DIR/exshoutify"
fi

# Create symlink untuk easy access
echo "[*] Creating symlink..."
ln -sf "$(pwd)" ~/music-downloader 2>/dev/null || true

# Test installation
echo ""
echo "[*] Testing installation..."
if exshoutify --help > /dev/null 2>&1; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                  ✓ INSTALLATION COMPLETED!                    ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "📍 Download locations:"
    echo "   ~/Music/Downloads          (Flat structure)"
    echo "   ~/Music/Organized          (Artist/Album structure)"
    echo ""
    echo "📝 Logs location:"
    echo "   ~/.music_downloader/logs"
    echo ""
    echo "🎵 Usage examples:"
    echo "   exshoutify 'https://open.spotify.com/track/...'"
    echo "   exshoutify 'https://www.youtube.com/watch?v=...'"
    echo "   exshoutify --batch urls.txt --parallel"
    echo "   exshoutify 'url' --organize --format flac"
    echo ""
    echo "✨ Start downloading now!"
    echo ""
else
    echo "[⚠] Installation completed but test failed"
    echo "Try running: exshoutify --help"
    exit 1
fi
