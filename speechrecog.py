#! /usr/bin/env python3

import io
import os
import tkinter as tk
from tkinter import filedialog, messagebox

import pyglet
import speech_recognition as sr
from gtts import gTTS

LESSON_PATH = "lessons\\"


def query_sphinx(audio, lang="en-US"):
    """Recognize speech using Sphinx

    Arguments:
    audio -- the audio that you want to analyze
    lang -- the language code comprised of ths ISO-630 language code (lower case)
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
    lang -- the language code comprised of ths ISO-630 language code (lower case)
            followed by a hypen and the ISO-3166 Country Code (upper case)
    
    Return the most likely text or None if nothing is understood
    """
    recognizer = sr.Recognizer()
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `recognizer.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
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
    # obtain audio from the microphone
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)
    return audio


class App:
    def __init__(
        self, master, method="sphinx", lang="en-US", phrasepack="greetings.txt"
    ):
        self.target = tk.StringVar()
        self.target_position = 0
        self.sr_meth = method
        self.lang = lang

        self.log = tk.StringVar(value="loading...")
        self.master = master
        self.phrasedict = dict()
        self.make_window()
        self.load_phraselist(phrasepack)

        self.change_sr(method)
        self.change_language(lang)

    def ulog(self, message, flag=None):
        self.log.set(message)

    def make_window(self):
        # Create the main window"
        self.master.winfo_toplevel().title("Pronunciation Trainer")
        self.main = tk.Frame(self.master)
        self.console = tk.Label(self.master, textvariable=self.log)
        self.main.pack(side=tk.TOP, fill=tk.X, expand=0)
        self.console.pack(side=tk.TOP, fill=tk.BOTH, expand=0)
        # Create the menu bar
        self.filebar = tk.Menu(self.master)
        self.filemenu = tk.Menu(self.filebar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.select_phraselist)
        self.filemenu.add_command(label="Quit", command=self.master.destroy)
        self.filebar.add_cascade(label="File", menu=self.filemenu)
        self.langmenu = tk.Menu(self.filebar, tearoff=0)
        self.langmenu.add_command(
            label="English", command=lambda: self.change_language("en-US")
        )
        self.langmenu.add_command(
            label="French", command=lambda: self.change_language("fr-FR")
        )
        self.filebar.add_cascade(label="Language", menu=self.langmenu)
        self.advmenu = tk.Menu(self.filebar, tearoff=0)
        self.srmenu = tk.Menu(self.advmenu, tearoff=0)
        self.srmenu.add_command(
            label="Sphinx", command=lambda: self.change_sr("sphinx")
        )
        self.srmenu.add_command(
            label="Google", command=lambda: self.change_sr("google")
        )
        self.advmenu.add_cascade(label="Speech Recognition", menu=self.srmenu)
        self.filebar.add_cascade(label="Advanced", menu=self.advmenu)
        self.master.config(menu=self.filebar)
        # Create the Main Interactive Area
        self.studio = tk.Frame(self.main)
        self.phrasebook = tk.Frame(self.main)
        self.studio.pack(side=tk.LEFT, fill=tk.Y)
        self.phrasebook.pack(side=tk.LEFT, fill=tk.X, expand=1)
        # Create the buttons and display for the Main Interactive Area
        self.listenButton = tk.Button(
            self.studio, text="Listen", width=25, command=self.play_example
        )
        self.speakButton = tk.Button(
            self.studio, text="Speak", width=25, command=self.speak
        )
        self.targetViewer = tk.Entry(
            self.studio,
            textvariable=self.target,
            justify=tk.CENTER,
            state="readonly",
            readonlybackground="white",
        )
        self.listenButton.pack(side=tk.TOP)
        self.speakButton.pack(side=tk.TOP)
        self.targetViewer.pack(side=tk.TOP)
        # Create and populate the phrases list
        self.phrases = tk.Listbox(self.phrasebook)
        self.phrases.bind("<Double-Button-1>", self.select_phrase)
        self.phrasescroll = tk.Scrollbar(self.phrasebook)
        self.phrases.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.phrasescroll.pack(side=tk.LEFT, fill=tk.Y)
        self.phrases.config(yscrollcommand=self.phrasescroll.set)
        self.phrasescroll.config(command=self.phrases.yview)

    def select_phrase(self, *args):
        self.targetViewer.config(readonlybackground="white")
        self.target_position = self.phrases.curselection()
        self.target.set(self.phrases.get(self.target_position))

    def play_example(self, *args):
        target = self.phrasedict[self.target.get()]
        filename = "resources/" + self.lang + "/" + target + ".mp3"
        # Try to load pre-recorded file
        if os.path.isfile(filename):
            a = pyglet.media.load(filename)
        else:  # Generate using TTS
            tts = gTTS(target, self.lang)
            tts.save(filename)
            a = pyglet.media.load(filename)
        a.play()

    def speak(self, *args):
        target = self.phrasedict[self.target.get()]
        audio = get_audio()
        if self.sr_meth == "sphinx":
            result = query_sphinx(audio, lang=self.lang)
        elif self.sr_meth == "google":
            result = query_google_speech(audio, lang=self.lang)

        if result == target:
            self.ulog("Good job!")
            self.phrases.itemconfig(self.target_position, {"bg": "green"})
            self.targetViewer.config(readonlybackground="green")
        else:
            self.ulog('I heard  "{}"! Try again!'.format(result))
            self.phrases.itemconfig(self.target_position, {"bg": "red"})
            self.targetViewer.config(readonlybackground="red")

    def select_phraselist(self):
        file = filedialog.askopenfile(
            parent=self.master,
            initialdir=LESSON_PATH + self.lang,
            mode="rb",
            title="Open Lesson...",
        )
        if file != None:
            self.load_phraselist(file)

    def load_phraselist(self, listname="test"):
        phrases = []
        if type(listname) == io.BufferedReader:
            try:
                data = listname.read().decode("latin1")
            except UnicodeDecodeError as e:
                print(type(listname.read()))
                data = str(listname.read())
                print(data, type(data))
            file = data.split("\n")
            for line in file:
                nline = line.rstrip("\n")
                nline = line.rstrip("\r")
                phrases.append(nline)
        else:
            self.ulog("Loading {}".format(self.lang + "\\" + listname))
            try:
                with open(LESSON_PATH + self.lang + "\\" + listname) as file:
                    for line in file:
                        nline = line.rstrip("\n")
                        phrases.append(nline)
            except FileNotFoundError:
                print("Language File Not Found")
                self.ulog(
                    "Error loading {}; loading default pack".format(listname)
                )
                phrases = [
                    "default package",
                    "hello",
                    "fine",
                    "what's up",
                    "merci",
                    "oui",
                    "non",
                ]
        packname, phrases = phrases[0], phrases[1:]
        self.phrases.delete(0, tk.END)
        for word in phrases:
            if word != "":
                try:
                    w = word.split(":")
                    self.phrases.insert(tk.END, w[0])
                    self.phrasedict[w[0]] = w[1]
                except IndexError as e:
                    print(word)
                    print("---")
                    print(phrases)
                    raise e
        # print(self.phrasedict)
        self.phrases.select_set(0)
        self.target.set(self.phrases.get(0))
        self.ulog("Loaded {}".format(packname))

    def change_language(self, lang="en-US"):
        # Remove checkmark from previously selected language
        if self.lang == "en-US":
            self.langmenu.entryconfigure(0, label="English")
        elif self.lang == "fr-FR":
            self.langmenu.entryconfigure(1, label="French")
        # Add checkmark to newly selected language
        if lang == "en-US":
            self.langmenu.entryconfigure(0, label="English " + "\u2713")
        elif lang == "fr-FR":
            self.langmenu.entryconfigure(1, label="French " + "\u2713")

        self.lang = lang
        self.ulog("Language changed to: {}".format(lang))

    def change_sr(self, sr_meth):
        # Remove checkmark from previously selected speech recognition method
        if self.sr_meth == "sphinx":
            self.srmenu.entryconfigure(0, label="Sphinx")
        elif self.sr_meth == "google":
            self.srmenu.entryconfigure(1, label="Google")
        # Add checkmark to newly selected speech recognition method
        if sr_meth == "sphinx":
            self.srmenu.entryconfigure(0, label="Sphinx " + "\u2713")
        elif sr_meth == "google":
            self.srmenu.entryconfigure(1, label="Google " + "\u2713")
        # Update speech recognition method
        self.sr_meth = sr_meth
        self.ulog("Switching to {} speech recognition".format(self.sr_meth))


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root, lang="en-US")
    root.mainloop()
