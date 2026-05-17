#!/bin/bash
set -e

echo "============================================"
echo " Arabic Voice Synthesis - Setup (Linux)"
echo "============================================"
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 not found. Install it with: sudo apt install python3 python3-pip"
    exit 1
fi

# Check ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "ffmpeg not found. Installing..."
    sudo apt update && sudo apt install -y ffmpeg
fi

echo "[1/3] Installing Python dependencies..."
pip3 install -r requirements.txt

echo
echo "[2/3] Preparing reference audio clip from audio.mp3..."
python3 prepare_reference.py

echo
echo "[3/3] Setup complete!"
echo
echo "To start the app, run:  python3 app.py"
echo "Then open:              http://localhost:5000"
