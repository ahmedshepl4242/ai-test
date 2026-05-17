import os
import uuid
from flask import Flask, request, jsonify, send_file, render_template
from TTS.api import TTS

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REFERENCE_AUDIO = os.path.join(BASE_DIR, "reference.wav")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load XTTS-v2 once at startup
print("Loading XTTS-v2 model (first run downloads ~2GB)...")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
print("Model ready.")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/synthesize", methods=["POST"])
def synthesize():
    data = request.get_json()
    text = (data or {}).get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    if not os.path.exists(REFERENCE_AUDIO):
        return jsonify({"error": "Reference audio not found. Run prepare_reference.py first."}), 500

    try:
        filename = f"{uuid.uuid4().hex}.wav"
        out_path = os.path.join(OUTPUT_DIR, filename)
        tts.tts_to_file(
            text=text,
            speaker_wav=REFERENCE_AUDIO,
            language="ar",
            file_path=out_path
        )
        return jsonify({"file": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/audio/<filename>")
def serve_audio(filename):
    path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(path):
        return jsonify({"error": "File not found"}), 404
    return send_file(path, mimetype="audio/wav")


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
