from langdetect import detect
from config import logger, TRANSLATION_LANG_CODES

class LanguageDetector:
    @staticmethod
    def detect_language_from_text(text):
        """Detect language from text."""
        try:
            detected = detect(text)
            logger.info(f"Language detected from text: {detected}")
            return detected
        except Exception as e:
            logger.warning(f"Language detection failed: {e}")
            return None

    @staticmethod
    def validate_language_detection(text, speech_lang, text_lang):
        """Validate detected language, preferring speech recognition unless clearly wrong."""
        speech_lang_std = TRANSLATION_LANG_CODES.get(speech_lang, speech_lang)
        if not text_lang or text_lang not in ['en', 'fr', 'ar']:
            logger.warning("Text language detection unreliable, using speech recognition language")
            return speech_lang_std
        if text_lang != speech_lang_std:
            logger.warning(f"Mismatch: Speech={speech_lang_std}, LangDetect={text_lang}")
            if len(text.split()) > 20 and text_lang != speech_lang_std:
                logger.info("Text is long enough to trust langdetect")
                return text_lang
            logger.info("Defaulting to speech recognition language")
            return speech_lang_std
        return text_lang