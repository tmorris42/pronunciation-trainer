"""Use sphinx speech-to-text"""
import speech_recognition as sr  # type: ignore


def query_sphinx(audio, lang="en-US"):
    """Recognize speech using Sphinx

    Arguments:
    audio -- the audio that you want to analyze
    lang -- language code comprised of ths ISO-630 language code (lowercase)
            followed by a hypen and the ISO-3166 Country Code (upper case)

    Return the recognized text or None if nothing is understood
    """
    recognizer = sr.Recognizer()
    try:
        text = recognizer.recognize_sphinx(audio, language=lang)
        print(f"Sphinx thinks you said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as error:
        print(f"Sphinx error; {error}")
    return None
