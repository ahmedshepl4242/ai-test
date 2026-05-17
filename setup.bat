@echo off
echo ============================================
echo  Arabic Voice Synthesis - Setup
echo ============================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

:: Check ffmpeg
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo ERROR: ffmpeg not found.
    echo Install it from https://ffmpeg.org/download.html
    echo Then add it to your PATH.
    pause
    exit /b 1
)

echo [1/3] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: pip install failed.
    pause
    exit /b 1
)

echo.
echo [2/3] Preparing reference audio clip from audio.mp3...
python prepare_reference.py
if errorlevel 1 (
    echo ERROR: Could not prepare reference audio.
    pause
    exit /b 1
)

echo.
echo [3/3] Setup complete!
echo.
echo To start the app, run:  python app.py
echo Then open:              http://localhost:5000
echo.
pause
