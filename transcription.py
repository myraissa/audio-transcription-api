import speech_recognition as sr
from config import logger, PREFERRED_LANGUAGES
from language_detection import LanguageDetector
class Transcriber:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def transcribe_audio_with_language(self, audio_data, language_code):
        """Transcribe audio data with a specific language code."""
        try:
            print(f"Trying transcription with: {language_code}")
            text = self.recognizer.recognize_google(audio_data, language=language_code) #type: ignore
            print(f"Transcription with {language_code} succeeded: {text[:60]}...")
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return None

    def transcribe_audio(self, audio_path):
        try:
            with sr.AudioFile(audio_path) as source:
                audio_data = self.recognizer.record(source)
                lang_detector = LanguageDetector()

                best_result = None

                for lang_code in PREFERRED_LANGUAGES:
                    text = self.transcribe_audio_with_language(audio_data, lang_code)
                    if text and len(text.split()) > 3:
                        text_lang = lang_detector.detect_language_from_text(text)
                        if text_lang == 'en':
                            return text, lang_code
                        if not best_result:
                            best_result = (text, lang_code)

                return best_result if best_result else (None, None)
        except Exception as e:
            logger.error(f"Error in transcription: {e}")
            return None, None