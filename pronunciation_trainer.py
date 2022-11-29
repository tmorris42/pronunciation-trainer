#! /usr/bin/env python3
"""A Pronunciation Trainer to help language learners improve"""

import io
import os
import tkinter as tk
from tkinter import filedialog

import pyglet  # type: ignore
import speech_recognition as sr  # type: ignore
from gtts import gTTS  # type: ignore

LESSON_PATH = "lessons"


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
        print("Sphinx error; {0}".format(error))
    return None


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
        print(
            "Google Speech Recognition thinks you said: {}".format(
                text["alternative"][0]["transcript"].lower()
            )
        )
        return text["alternative"][0]["transcript"].lower()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as error:
        print(f"Could not request results from Google service; {error}")
    except TypeError as error:
        print("here is the problem text\n---\n", text)
        raise error
    return None


def get_audio():
    """Obtain audio from the microphone"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)
    return audio


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
        self.phrase_dictionary = dict()
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
                with open(filepath) as file:
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


class App:
    """Speech Recognition app from improving pronunciation"""

    def __init__(self, master, lang="en-US", phrasepack="greetings.txt"):
        self.target = tk.StringVar()
        self.log = tk.StringVar(value="loading...")
        self.master = master
        self.make_window()

        self.trainer = Trainer()
        self.load_phraselist(phrasepack)
        self.change_sr("sphinx")
        self.change_language(lang)

    def ulog(self, message):
        """Log a message to the info box"""
        self.log.set(message)

    def make_window(self):
        """Create the main window"""
        self.master.winfo_toplevel().title("Pronunciation Trainer")
        main_frame = tk.Frame(self.master)
        log_display = tk.Label(self.master, textvariable=self.log)
        main_frame.pack(side=tk.TOP, fill=tk.X, expand=0)
        log_display.pack(side=tk.TOP, fill=tk.BOTH, expand=0)
        # Create the menu bar
        filebar = tk.Menu(self.master)
        filemenu = tk.Menu(filebar, tearoff=0)
        filemenu.add_command(label="Open", command=self.select_phraselist)
        filemenu.add_command(label="Quit", command=self.master.destroy)
        filebar.add_cascade(label="File", menu=filemenu)
        self.langmenu = tk.Menu(filebar, tearoff=0)
        self.langmenu.add_command(
            label="English", command=lambda: self.change_language("en-US")
        )
        self.langmenu.add_command(
            label="French", command=lambda: self.change_language("fr-FR")
        )
        filebar.add_cascade(label="Language", menu=self.langmenu)
        advanced_menu = tk.Menu(filebar, tearoff=0)
        self.srmenu = tk.Menu(advanced_menu, tearoff=0)
        self.srmenu.add_command(
            label="Sphinx", command=lambda: self.change_sr("sphinx")
        )
        self.srmenu.add_command(
            label="Google", command=lambda: self.change_sr("google")
        )
        advanced_menu.add_cascade(label="Speech Recognition", menu=self.srmenu)
        filebar.add_cascade(label="Advanced", menu=advanced_menu)
        self.master.config(menu=filebar)
        # Create the Main Interactive Area
        studio_frame = tk.Frame(main_frame)
        phrasebook_frame = tk.Frame(main_frame)
        studio_frame.pack(side=tk.LEFT, fill=tk.Y)
        phrasebook_frame.pack(side=tk.LEFT, fill=tk.X, expand=1)
        # Create the buttons and display for the Main Interactive Area
        listen_button = tk.Button(
            studio_frame, text="Listen", width=25, command=self.play_example
        )
        speak_button = tk.Button(
            studio_frame, text="Speak", width=25, command=self.speak
        )
        self.target_viewer = tk.Entry(
            studio_frame,
            textvariable=self.target,
            justify=tk.CENTER,
            state="readonly",
            readonlybackground="white",
        )
        listen_button.pack(side=tk.TOP)
        speak_button.pack(side=tk.TOP)
        self.target_viewer.pack(side=tk.TOP)
        # Create and populate the phrases list
        self.phrases = tk.Listbox(phrasebook_frame)
        self.phrases.bind("<Double-Button-1>", self.select_phrase)
        self.phrasescroll = tk.Scrollbar(phrasebook_frame)
        self.phrases.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.phrasescroll.pack(side=tk.LEFT, fill=tk.Y)
        self.phrases.config(yscrollcommand=self.phrasescroll.set)
        self.phrasescroll.config(command=self.phrases.yview)

    def select_phrase(self, *_, **__):
        """Select a word from the phrase list"""
        self.target_viewer.config(readonlybackground="white")
        target_position = self.phrases.curselection()
        self.target.set(self.phrases.get(target_position))

    def play_example(self):
        """Play a TTS example of the current word in the current language"""
        target = self.trainer.phrase_dictionary[self.target.get()]
        self.trainer.play_example(target)

    def speak(self):
        """Listen for speech, send to current speech_recognition"""
        target = self.trainer.phrase_dictionary[
            self.target.get()
        ]  # *** Handle more clearly? "get target?"
        correct, response = self.trainer.speak(target)

        target_position = self.phrases.curselection()
        if correct:
            self.ulog("Good job!")
            self.phrases.itemconfig(target_position, {"bg": "green"})
            self.target_viewer.config(readonlybackground="green")
        else:
            self.ulog('I heard  "{}"! Try again!'.format(response))
            self.phrases.itemconfig(target_position, {"bg": "red"})
            self.target_viewer.config(readonlybackground="red")

    def select_phraselist(self):
        """Open the file dialog to select a phrase list"""
        file = filedialog.askopenfile(
            parent=self.master,
            initialdir=LESSON_PATH + self.trainer.language,
            mode="rb",
            title="Open Lesson...",
        )
        if file is not None:
            self.load_phraselist(file)

    def load_phraselist(self, phraselist=None):
        """Load a list of phrase for pronunciation practice"""
        if phraselist is not None:
            self.trainer.load_phrases(phraselist)
        self.phrases.delete(0, tk.END)
        for key in self.trainer.phrases:
            self.phrases.insert(tk.END, key)
        self.phrases.select_set(0)
        self.target.set(self.phrases.get(0))
        self.ulog("Loaded {self.trainer.phrases['__PACKNAME__']}")

    def change_language(self, lang="en-US"):
        """Change speech recognition language and update menus"""
        # Remove checkmark from previously selected language
        if self.trainer.language == "en-US":
            self.langmenu.entryconfigure(0, label="English")
        elif self.trainer.language == "fr-FR":
            self.langmenu.entryconfigure(1, label="French")
        # Add checkmark to newly selected language
        if lang == "en-US":
            self.langmenu.entryconfigure(0, label="English " + "\u2713")
        elif lang == "fr-FR":
            self.langmenu.entryconfigure(1, label="French " + "\u2713")

        self.trainer.language = lang
        self.ulog("Language changed to: {}".format(lang))

    def change_sr(self, sr_meth):
        """Change speech recognition method and update menus"""
        # Remove checkmark from previously selected speech recognitiongg method
        if self.trainer.speech_recognition_method == "sphinx":
            self.srmenu.entryconfigure(0, label="Sphinx")
        elif self.trainer.speech_recognition_method == "google":
            self.srmenu.entryconfigure(1, label="Google")
        # Add checkmark to newly selected speech recognition method
        if sr_meth == "sphinx":
            self.srmenu.entryconfigure(0, label="Sphinx " + "\u2713")
        elif sr_meth == "google":
            self.srmenu.entryconfigure(1, label="Google " + "\u2713")
        # Update speech recognition method
        self.trainer.speech_recognition_method = sr_meth
        self.ulog("Switching to {} speech recognition".format(sr_meth))


if __name__ == "__main__":
    ROOT = tk.Tk()
    APP = App(ROOT, lang="en-US")
    ROOT.mainloop()
