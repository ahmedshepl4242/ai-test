"""
Extracts a clean 10-second reference clip from audio.mp3 for voice cloning.
Run this once before starting the web app.
"""

import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(BASE_DIR, "audio.mp3")
OUTPUT = os.path.join(BASE_DIR, "reference.wav")
DURATION = 10  # seconds — Chatterbox works best with ~10s


def extract_reference():
    if not os.path.exists(INPUT):
        print(f"ERROR: Could not find {INPUT}")
        sys.exit(1)

    print(f"Extracting {DURATION}s reference clip from {INPUT} ...")
    result = subprocess.run([
        "ffmpeg", "-y",
        "-i", INPUT,
        "-t", str(DURATION),
        "-ac", "1",          # mono
        "-ar", "22050",      # 22kHz — good for TTS
        OUTPUT
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print("ffmpeg error:\n", result.stderr)
        sys.exit(1)

    print(f"Reference clip saved to: {OUTPUT}")


if __name__ == "__main__":
    extract_reference()
