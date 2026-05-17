#!/bin/bash
set -e

echo "============================================"
echo " Arabic Voice Synthesis - Setup (Linux)"
echo "============================================"
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 not found."
    echo "Install with: sudo apt install python3 python3-venv python3-full"
    exit 1
fi

# Check ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "ffmpeg not found. Installing..."
    sudo apt update && sudo apt install -y ffmpeg
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

echo "[1/3] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo
echo "[2/3] Preparing reference audio clip from audio.mp3..."
python prepare_reference.py

echo
echo "[3/3] Setup complete!"
echo
echo "To start the app run:"
echo "  source venv/bin/activate && python app.py"
echo "Then open: http://localhost:5000"
