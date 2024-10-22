import speech_recognition as sr

def speak():
    
    # Initialize recognizer
    recognizer = sr.Recognizer()

    while True:
        # Use microphone as source
        with sr.Microphone() as source:
            print("Say something:")
            audio = recognizer.listen(source)

        # Recognize speech using Google Web Speech API
        try:
            text = recognizer.recognize_google(audio)

            print(f"You said: {text}")

            return text

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

if __name__ == "__main__":
    speak()