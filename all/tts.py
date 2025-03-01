# tts.py
import os
from pathlib import Path
import openai
import logging
from gtts import gTTS  # Ensure gTTS is installed (pip install gTTS)

# Set OpenAI API key from the environment variable
openai.api_key = os.getenv("api_key_oai")

def text_to_speech(text: str, voice: str = "coral", model: str = "tts-1") -> str:
    """
    Convert input text to speech using OpenAI's TTS API.
    Falls back to gTTS if the OpenAI API fails.
    
    Returns:
        The file path to the generated audio file.
    """
    # Generate a unique filename using a hash of the text
    output_file = Path(__file__).parent / 'output' / f"speech_{abs(hash(text))}.pus"
    try:
        response = openai.Audio.speech.create(
            model=model,
            voice=voice,
            input=text,
        )
        response.stream_to_file(str(output_file))
        logging.info("OpenAI TTS succeeded.")
        return str(output_file)
    except Exception as e:
        logging.error("OpenAI TTS failed, falling back to gTTS. Error: %s", e)
        return text_to_speech_gtts(text)

def text_to_speech_gtts(text: str) -> str:
    """
    Convert input text to speech using gTTS.
    
    Returns:
        The file path to the generated audio file.
    """
    output_file = Path(__file__).parent / 'output' / f"speech_{abs(hash(text))}.mp3"
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(str(output_file))
        logging.info("gTTS succeeded.")
        return str(output_file)
    except Exception as e:
        logging.error("gTTS failed. Error: %s", e)
        raise

def generate_audio(text: str) -> str:
    """
    Converts the provided text to speech and returns the path of the audio file.
    """
    if text:
        try:
            audio_file = text_to_speech(text)
            log_info("Audio generated successfully.")
            return audio_file
        except Exception as e:
            log_error(f"Audio generation failed: {e}")
            return ""
    log_error("No text provided for TTS.")
    return ""