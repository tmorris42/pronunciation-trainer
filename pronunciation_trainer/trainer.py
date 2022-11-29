"""The core for the pronunciation trainer"""
import io
import os

import pyglet  # type: ignore
from gtts import gTTS  # type: ignore

from .apis import query_google_speech, query_sphinx
from .get_audio import get_audio

LESSON_PATH = "lessons"


class Trainer:
    """Core for the pronunciation trainer"""

    def __init__(self, lang="en-US", phrasepack=None, sr_method="sphinx"):
        self.language = lang
        self.speech_recognition_method = sr_method
        if phrasepack is not None:
            self.phrase_dictionary = self.load_phrases(phrasepack)
        else:
            self.phrase_dictionary = {"__PACKNAME__": None}

    @property
    def phrases(self):
        """Generate currently loaded phrases"""
        for phrase in self.phrase_dictionary:
            if phrase[:2] != "__":
                yield phrase

    @property
    def package_name(self):
        """Return package name"""
        return self.phrase_dictionary["__PACKNAME__"]

    def load_phrases(self, filename):
        """Load phrases from file

        Return dictionary
        """
        phrases = []
        self.phrase_dictionary = {}
        if isinstance(filename, io.BufferedReader):
            try:
                data = filename.read().decode("latin1")
            except UnicodeDecodeError:
                print(type(filename.read()))
                data = str(filename.read())
                print(data, type(data))
            file = data.split("\n")
            for line in file:
                nline = line.rstrip("\n")
                nline = line.rstrip("\r")
                phrases.append(nline)
        else:
            filepath = os.path.join(LESSON_PATH, self.language, filename)
            try:
                with open(filepath, encoding="utf-8") as file:
                    for line in file:
                        phrases.append(line.rstrip("\n"))
            except FileNotFoundError:
                print(f"Language File Not Found at {filepath}")
                return self.phrase_dictionary
        self.phrase_dictionary["__PACKNAME__"] = phrases[0]
        for word in phrases[1:]:
            if word != "":
                try:
                    word_translation = word.split(":")
                    self.phrase_dictionary[
                        word_translation[0]
                    ] = word_translation[1]
                except IndexError as error:
                    print(f"{word}\n---\n{phrases}")
                    raise error
        return self.phrase_dictionary

    def play_example(self, target):
        """Play a TTS example of the current word in the current language"""
        if not os.path.isdir(os.path.join("resources", self.language)):
            os.makedirs(os.path.join(".", "resources", self.language))
        filename = "resources/" + self.language + "/" + target + ".mp3"
        # Try to load pre-recorded file
        if os.path.isfile(filename):  # *** Change to try/except
            audio = pyglet.media.load(filename)
        else:  # Generate using TTS
            tts = gTTS(text=target, lang=self.language)
            tts.save(filename)
            audio = pyglet.media.load(filename)
        audio.play()

    def speak(self, target):
        """Listen for speech, send to current speech_recognition"""
        audio = get_audio()
        if self.speech_recognition_method == "sphinx":
            result = query_sphinx(audio, lang=self.language)
        elif self.speech_recognition_method == "google":
            result = query_google_speech(audio, lang=self.language)

        if result == target:
            return True, result
        return False, result
