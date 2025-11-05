from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import tempfile
from typing import Optional, Dict, Any

# Import your existing modules
from transcription import Transcriber
from audio_processor import AudioProcessor
from language_detection import LanguageDetector
from config import logger

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
ALLOWED_AUDIO_EXTENSIONS = {'.wav', '.mp3', '.m4a', '.flac', '.ogg', '.aac'}
ALLOWED_VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'}
ALLOWED_EXTENSIONS = ALLOWED_AUDIO_EXTENSIONS | ALLOWED_VIDEO_EXTENSIONS

# Initialize processors
transcriber = Transcriber()
audio_processor = AudioProcessor()
language_detector = LanguageDetector()

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

def create_response(success: bool, text: Optional[str] = None, 
                   detected_language: Optional[str] = None,
                   language_code: Optional[str] = None,
                   word_count: Optional[int] = None,
                   error: Optional[str] = None) -> Dict[str, Any]:
    """Create standardized response"""
    return {
        'success': success,
        'text': text,
        'detected_language': detected_language,
        'language_code': language_code,
        'word_count': word_count,
        'error': error
    }

@app.route('/', methods=['GET'])
def health_check():
    """API health check endpoint"""
    return jsonify({
        'status': 'online',
        'service': 'Audio Transcription API',
        'version': '1.0.0'
    })

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
  
    temp_file_path = None
    temp_audio_path = None
    
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify(create_response(
                success=False,
                error='No file provided'
            )), 400
        
        file = request.files['file']
        
        # Check if file has a name
        if file.filename == '':
            return jsonify(create_response(
                success=False,
                error='No file selected'
            )), 400
        
        # Validate file extension
        if not file.filename:
            return jsonify(create_response(
                success=False,
                error='No file selected'
            )), 400

        filename = secure_filename(file.filename or "")

        suffix = os.path.splitext(filename)[1]
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file_path = temp_file.name
            file.save(temp_file_path)
        
        logger.info(f"Processing file: {filename}")
        
        # Process based on file type
        if suffix.lower() in ALLOWED_VIDEO_EXTENSIONS:
            # Extract audio from video
            temp_audio_path = temp_file_path.replace(suffix, '_audio.wav')
            audio_path = audio_processor.extract_audio_from_video(
                temp_file_path, 
                temp_audio_path
            )
            if not audio_path:
                return jsonify(create_response(
                    success=False,
                    error='Failed to extract audio from video'
                )), 500
        
        elif suffix.lower() in ALLOWED_AUDIO_EXTENSIONS:
            # Convert audio to WAV format for consistency
            temp_audio_path = temp_file_path.replace(suffix, '_audio.wav')
            audio_path = audio_processor.extract_audio_from_video(
                temp_file_path, 
                temp_audio_path
            )
            if not audio_path:
                return jsonify(create_response(
                    success=False,
                    error='Failed to process audio file'
                )), 500
        else:
            return jsonify(create_response(
                success=False,
                error=f'Unsupported file format: {suffix}'
            )), 400
        
        # Transcribe audio
        text, lang_code = transcriber.transcribe_audio(audio_path)
        
        if not text:
            return jsonify(create_response(
                success=False,
                error='Could not transcribe audio. The audio may be unclear or in an unsupported language.'
            )), 200
        
        # Detect language from text for validation
        text_lang = language_detector.detect_language_from_text(text)
        validated_lang = language_detector.validate_language_detection(
            text, lang_code, text_lang
        )
        
        word_count = len(text.split())
        
        logger.info(f"Transcription successful: {word_count} words, language: {validated_lang}")
        
        return jsonify(create_response(
            success=True,
            text=text,
            detected_language=validated_lang,
            language_code=lang_code,
            word_count=word_count
        )), 200
        
    except Exception as e:
        logger.error(f"Error in transcription endpoint: {e}")
        return jsonify(create_response(
            success=False,
            error=f'Internal server error: {str(e)}'
        )), 500
    
    finally:
        # Cleanup temporary files
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception as e:
                logger.warning(f"Failed to remove temp file: {e}")
        
        if temp_audio_path and os.path.exists(temp_audio_path):
            try:
                os.remove(temp_audio_path)
            except Exception as e:
                logger.warning(f"Failed to remove audio file: {e}")

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify(create_response(
        success=False,
        error='File too large. Maximum size is 100MB'
    )), 413

@app.errorhandler(500)
def internal_server_error(error):
    """Handle internal server error"""
    return jsonify(create_response(
        success=False,
        error='Internal server error'
    )), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)