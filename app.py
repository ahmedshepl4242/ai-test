import os
import uuid
import torchaudio
from flask import Flask, request, jsonify, send_file, render_template
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

app = Flask(__name__)

REFERENCE_AUDIO = r"E:\ai-audio\reference.wav"
OUTPUT_DIR = r"E:\ai-audio\outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load multilingual model once at startup (CPU mode)
print("Loading Chatterbox Multilingual model (this may take a minute on CPU)...")
model = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
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
        wav = model.generate(text, audio_prompt_path=REFERENCE_AUDIO, language_id="ar")
        filename = f"{uuid.uuid4().hex}.wav"
        out_path = os.path.join(OUTPUT_DIR, filename)
        torchaudio.save(out_path, wav, model.sr)
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
