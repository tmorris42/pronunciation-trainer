"""Use google speech-to-text"""
import speech_recognition as sr  # type: ignore


def query_google_speech(audio, lang="en-US"):
    """Recognize speech using Google Speech Recognition

    Arguments:
    audio -- the audio that you want to analyze
    lang -- language code comprised of ths ISO-630 language code (lowercase)
            followed by a hypen and the ISO-3166 Country Code (uppercase)

    Return the most likely text or None if nothing is understood
    """
    recognizer = sr.Recognizer()
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use
        # `recognizer.recognize_google(
        # audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `recognizer.recognize_google(audio)
        text = recognizer.recognize_google(audio, show_all=True, language=lang)
        readable_text = text["alternative"][0]["transcript"].lower()
        print(f"Google Speech Recognition thinks you said: {readable_text}")
        return readable_text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as error:
        print(f"Could not request results from Google service; {error}")
    except TypeError as error:
        print("here is the problem text\n---\n", text)
        raise error
    return None
