import os
import tempfile
import time
from gtts import gTTS
import playsound  # Cross-platform audio playback


class AudioGenerator:
    """A simple Text-to-Speech class using Google TTS."""

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

    def say(self, text, save_to_file=None):
        """
        Speak text aloud and optionally save to file.

        Args:
            text (str): Text to convert to speech
            save_to_file (str, optional): Output filename (e.g., 'output.mp3')
        """
        try:
            # Generate speech
            tts = gTTS(text=text, lang=self.lang, slow=self.slow)

            # Save to temp file (or specified file)
            if save_to_file:
                output_file = save_to_file
                tts.save(output_file)
                print(f"Saved to: {os.path.abspath(output_file)}")
            else:
                with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
                    output_file = fp.name
                    tts.save(output_file)

                    # Play audio
                    self._play_audio(output_file)

        except Exception as e:
            print(f"Error in TTS: {e}")
            if self._is_internet_connected():
                print("Retrying...")
                time.sleep(1)
                self.say(text, save_to_file)
            else:
                print("No internet connection detected.")

    def _play_audio(self, file_path):
        """Play audio file using playsound (cross-platform)."""
        try:
            playsound.playsound(file_path, block=True)
        except Exception as e:
            print(f"Playback error: {e}")

    def _is_internet_connected(self):
        """Check internet connection (crude method)."""
        try:
            import urllib.request
            urllib.request.urlopen("https://www.google.com", timeout=2)
            return True
        except:
            return False


# ===== Example Usage =====
if __name__ == "__main__":
    # Initialize with British English
#     tts = AudioGenerator(lang="en-uk", slow=False)

#     text_to_say = """
# these are the 
# types of files
# that you can
# export the
# data as
#                 """

#     # Speak immediately
#     tts.say(text_to_say)

#     # Save to file and then play
#     tts.say(text_to_say, save_to_file="output.mp3")

#     # Non-English example (Spanish)
#     # tts_es = AudioGenerator(lang="es")
#     # tts_es.say("Hola desde el traductor de Google")
