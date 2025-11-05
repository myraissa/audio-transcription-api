# 🧠 Audio Transcription API

A lightweight Flask-based API for audio and video transcription. It supports multiple audio and video formats, automatically extracts audio, performs transcription, and detects the spoken language.

## 🚀 Features

- 🎙️ Transcribe audio and video files (.mp3, .wav, .mp4, etc.)
- 🧩 Automatic language detection and validation
- 🪄 Handles large files up to 100 MB
- 🔄 Returns transcribed text, language code, and word count
- 🌍 Built with Flask and CORS enabled for web integration
- ⚙️ Modular structure with reusable processors

## 🏗️ Project Structure

```
project/
│
├── app.py                     # Main Flask API
├── transcription.py           # Handles audio transcription logic
├── audio_processor.py         # Extracts/Processes audio from files
├── language_detection.py      # Detects and validates text language
├── config.py                  # Logger and configuration setup
│
├── requirements.txt           # Python dependencies
└── README.md                  # Documentation
```

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # On Linux/macOS
.venv\Scripts\activate         # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Run the API

```bash
python app.py
```

The server will start at: **http://localhost:8000**

## 🧪 API Endpoints

### ✅ Health Check

**GET /**

**Response:**

```json
{
  "status": "online",
  "service": "Audio Transcription API",
  "version": "1.0.0"
}
```

### 🎧 Transcribe Audio or Video

**POST /transcribe**

Send a file (audio or video) as form-data under the key `"file"`.

**Example using curl:**

```bash
curl -X POST -F "file=@example.mp3" http://localhost:8000/transcribe
```

**Response:**

```json
{
  "success": true,
  "text": "This is the transcribed text.",
  "detected_language": "en",
  "language_code": "en",
  "word_count": 6
}
```

**Error Example:**

```json
{
  "success": false,
  "error": "Unsupported file format: .txt"
}
```

## ⚠️ Error Handling

| Status | Message | Description |
|--------|---------|-------------|
| 400 | No file provided | Missing upload |
| 413 | File too large | File exceeds 100MB |
| 500 | Internal server error | Unexpected exception |

## 🧰 Technologies

- **Flask** – Backend framework
- **Werkzeug** – File management utilities
- **CORS** – Cross-origin support
- **FFmpeg** (via AudioProcessor) – Audio extraction
- **Language Detection & Transcription Modules** – Custom logic

## 👩‍💻 Developer Notes

- Modify `MAX_CONTENT_LENGTH` to change upload limits.
- Extend `ALLOWED_EXTENSIONS` to support more formats.
- Transcriber, AudioProcessor, and LanguageDetector should be implemented modularly.
