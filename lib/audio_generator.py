import io
from gtts import gTTS
import requests
import tempfile

class AudioGenerator:
    """A Text-to-Speech class with streaming support using Google TTS."""

    def __init__(self, lang="en", slow=False, timeout=10):
        """
        Initialize TTS engine.

        Args:
            lang (str): Language code (e.g., 'en', 'es', 'fr')
            slow (bool): Slow speech for clearer pronunciation
            timeout (int): Max seconds to wait for API response
        """
        self.lang = lang
        self.slow = slow
        self.timeout = timeout

    def generate_to_stream(self, text):
        """
        Generate speech and return as in-memory bytes stream.

        Args:
            text (str): Text to convert to speech

        Returns:
            io.BytesIO: Audio data in memory
        """
        try:
            # Create in-memory buffer
            audio_buffer = io.BytesIO()
            
            # Generate speech directly to buffer
            tts = gTTS(text=text, lang=self.lang, slow=self.slow)
            tts.write_to_fp(audio_buffer)
            
            # Reset buffer position to start
            audio_buffer.seek(0)
            return audio_buffer

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"TTS API request failed: {e}")
        except Exception as e:
            raise RuntimeError(f"TTS generation error: {e}")

    # Keeping the original file-based methods for compatibility
    def say(self, text, save_to_file=None):
        """Maintained for backward compatibility."""
        if save_to_file:
            self._save_to_file(text, save_to_file)
        else:
            audio_buffer = self.generate_to_stream(text)
            self._play_from_buffer(audio_buffer)

    def _save_to_file(self, text, filename):
        """Save generated speech to file."""
        tts = gTTS(text=text, lang=self.lang, slow=self.slow)
        tts.save(filename)

    def _play_from_buffer(self, audio_buffer):
        """Play audio from in-memory buffer."""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as tmp:
                # Write buffer to temp file
                tmp.write(audio_buffer.read())
                tmp.flush()
                # Play the temp file
                playsound.playsound(tmp.name, block=True)
        except Exception as e:
            print(f"Playback error: {e}")