import os
from pydub import AudioSegment
from config import logger

class AudioProcessor:
    @staticmethod
    def extract_audio_from_video(video_path, audio_output="temp_audio.wav"):
        """Extract audio from video file."""
        try:
            audio = AudioSegment.from_file(video_path)
            audio.export(audio_output, format="wav")
            logger.info(f"Audio extracted: {audio_output}, duration: {len(audio) / 1000:.2f}s")
            return audio_output
        except Exception as e:
            logger.error(f"Error extracting audio: {e}")
            return None