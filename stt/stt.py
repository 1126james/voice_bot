import speech_recognition as sr

# Dictionary to store language-locale pairs
language_locales = {
    "english": "en-US",
    "chinese": "zh-CN",
    "cantonese": "yue-Hant-HK",
    "japanese": "ja-JP"
}

def speak(language):
    
    # Initialize recognizer
    recognizer = sr.Recognizer()

    recognizer.pause_threshold = 0.7

    while True:
        # Use microphone as source
        with sr.Microphone() as source:
            print(f"Say something in {language}:")

            # Calibrate the recognizer for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            # Set the minimum audio energy threshold
            recognizer.energy_threshold = 3000  # Adjust this value as needed

            audio = recognizer.listen(source)

        # Recognize speech using Google Web Speech API
        try:
            locale = language_locales.get(language.lower())
            if locale:
                text = recognizer.recognize_google(audio, language=locale)
                print(f"You said: {text}")
                return text
            else:
                print("Unsupported language")
                return

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

def get_supported_languages():
    return ", ".join(language_locales.keys())