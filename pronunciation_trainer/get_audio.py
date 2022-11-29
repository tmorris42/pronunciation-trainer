"""Function to get audio from the microphone"""
import speech_recognition as sr  # type: ignore


def get_audio():
    """Obtain audio from the microphone"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)
    return audio
