import requests
import simpleaudio as sa
from io import BytesIO

def play_tts(language: str = 'ja', text: str = '') -> bool:
    """
    Send text to TTS API and play the resulting audio
    Args:
        language (str): Language code ('ja', 'en', 'zh'). Defaults to 'ja'
        text (str): Text to be converted to speech
    Returns:
        bool: True if successful, False if failed
    """
    url = "http://127.0.0.1:9880"
    params = {
        "text": text,
        "text_language": language,
        "cut_punc": "、。" if language == 'ja' else ",."
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            wave_obj = sa.WaveObject.from_wave_file(BytesIO(response.content))
            play_obj = wave_obj.play()
            play_obj.wait_done()
            return True
        else:
            print(f"TTS API request failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error playing TTS audio: {str(e)}")
        return False