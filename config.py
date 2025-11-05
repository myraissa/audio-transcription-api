import logging

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Language configurations
PREFERRED_LANGUAGES = [
    'en-US',  # English (US)
    'fr-FR',  # French (France)
    'ar-SA',  # Arabic (Saudi Arabia)
    
]

TRANSLATION_LANG_CODES = {
    'ar-SA': 'ar',
    'en-US': 'en',
    'fr-FR': 'fr',
    'fr': 'fr',
    'en': 'en',
    'ar': 'ar'
}

# File upload limits
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_AUDIO_EXTENSIONS = ['.wav', '.mp3', '.m4a', '.flac', '.ogg', '.aac']
ALLOWED_VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']