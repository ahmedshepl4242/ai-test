"""
Finds and extracts the best 10-second reference clip from audio.mp3 for voice cloning.
Scores windows by: speech density, energy consistency, and low silence ratio.
Run this once before starting the web app.
"""

import os
import sys
import subprocess
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(BASE_DIR, "audio.mp3")
OUTPUT = os.path.join(BASE_DIR, "reference.wav")
WINDOW_SEC = 30
SAMPLE_RATE = 22050


def load_audio_numpy(path):
    """Use ffmpeg to decode audio to raw PCM float32 numpy array."""
    cmd = [
        "ffmpeg", "-y", "-i", path,
        "-ac", "1", "-ar", str(SAMPLE_RATE),
        "-f", "f32le", "-"
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print("ffmpeg error:", result.stderr.decode())
        sys.exit(1)
    audio = np.frombuffer(result.stdout, dtype=np.float32)
    return audio


def score_window(chunk, sr):
    """
    Score a chunk of audio. Higher = better reference material.
    Criteria:
      - High average energy (person is speaking clearly)
      - Low silence ratio (< 20% of frames are near-silent)
      - Consistent energy (low std deviation relative to mean = steady voice)
    """
    frame_size = sr // 100  # 10ms frames
    frames = [chunk[i:i+frame_size] for i in range(0, len(chunk) - frame_size, frame_size)]
    energies = np.array([np.sqrt(np.mean(f**2)) for f in frames])

    silence_threshold = 0.01
    silence_ratio = np.mean(energies < silence_threshold)
    avg_energy = np.mean(energies)
    energy_std = np.std(energies)
    consistency = avg_energy / (energy_std + 1e-6)  # higher = more consistent

    # Penalize windows with too much silence
    if silence_ratio > 0.25:
        return -1.0

    score = avg_energy * 10 + consistency * 0.5
    return float(score)


def find_best_window(audio, sr, window_sec=10):
    window_samples = sr * window_sec
    step_samples = sr * 2  # check every 2 seconds

    best_score = -999
    best_start = 0

    for start in range(0, len(audio) - window_samples, step_samples):
        chunk = audio[start:start + window_samples]
        s = score_window(chunk, sr)
        if s > best_score:
            best_score = s
            best_start = start

    best_time = best_start / sr
    print(f"Best window found at {best_time:.1f}s (score: {best_score:.3f})")
    return best_time


def extract_clip(start_sec, duration_sec=10):
    cmd = [
        "ffmpeg", "-y",
        "-i", INPUT,
        "-ss", str(start_sec),
        "-t", str(duration_sec),
        "-ac", "1",
        "-ar", str(SAMPLE_RATE),
        OUTPUT
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("ffmpeg error:", result.stderr)
        sys.exit(1)


def main():
    if not os.path.exists(INPUT):
        print(f"ERROR: Could not find {INPUT}")
        sys.exit(1)

    print(f"Analyzing {INPUT} to find best {WINDOW_SEC}s reference clip...")
    audio = load_audio_numpy(INPUT)
    print(f"Audio loaded: {len(audio)/SAMPLE_RATE:.1f}s total")

    best_start = find_best_window(audio, SAMPLE_RATE, WINDOW_SEC)
    extract_clip(best_start, WINDOW_SEC)
    print(f"Reference clip saved to: {OUTPUT}")


if __name__ == "__main__":
    main()
