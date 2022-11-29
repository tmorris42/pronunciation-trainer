#! /usr/bin/env python3
"""A Pronunciation Trainer to help language learners improve"""


import tkinter as tk


from .trainer import Trainer
from .components.MainWindow import MainWindow

LESSON_PATH = "lessons"


class App:
    """Speech Recognition app from improving pronunciation"""

    def __init__(self, master, lang="en-US", phrasepack="greetings.txt"):
        self.window = MainWindow(master, listen_callback=self.play_example, speak_callback=self.speak)

        self.trainer = Trainer()
        self.load_phraselist(phrasepack)
        self.change_sr("sphinx")
        self.change_language(lang)

    def ulog(self, message):
        """Log a message to the info box"""
        self.window.log.set(message)

    def play_example(self):
        """Play a TTS example of the current word in the current language"""
        target = self.trainer.phrase_dictionary[self.window.target.get()]
        self.trainer.play_example(target)

    def speak(self):
        """Listen for speech, send to current speech_recognition"""
        target = self.trainer.phrase_dictionary[
            self.window.target.get()
        ]  # *** Handle more clearly? "get target?"
        correct, response = self.trainer.speak(target)

        target_position = self.window.phrases.curselection()
        if correct:
            self.ulog("Good job!")
            self.window.phrases.itemconfig(target_position, {"bg": "green"})
            self.window.target_viewer.config(readonlybackground="green")
        else:
            self.ulog(f'I heard  "{response}"! Try again!')
            self.window.phrases.itemconfig(target_position, {"bg": "red"})
            self.window.target_viewer.config(readonlybackground="red")

    def load_phraselist(self, phraselist=None):
        """Load a list of phrase for pronunciation practice"""
        if phraselist is not None:
            self.trainer.load_phrases(phraselist)
        self.window.phrases.delete(0, tk.END)
        for key in self.trainer.phrases:
            self.window.phrases.insert(tk.END, key)
        self.window.phrases.select_set(0)
        self.window.target.set(self.window.phrases.get(0))
        self.ulog("Loaded {self.trainer.phrases['__PACKNAME__']}")

    def change_language(self, lang="en-US"):
        """Change speech recognition language and update menus"""
        # Remove checkmark from previously selected language
        if self.trainer.language == "en-US":
            self.window.langmenu.entryconfigure(0, label="English")
        elif self.trainer.language == "fr-FR":
            self.window.langmenu.entryconfigure(1, label="French")
        # Add checkmark to newly selected language
        if lang == "en-US":
            self.window.langmenu.entryconfigure(0, label="English " + "\u2713")
        elif lang == "fr-FR":
            self.window.langmenu.entryconfigure(1, label="French " + "\u2713")

        self.trainer.language = lang
        self.ulog(f"Language changed to: {lang}")

    def change_sr(self, sr_meth):
        """Change speech recognition method and update menus"""
        # Remove checkmark from previously selected speech recognitiongg method
        if self.trainer.speech_recognition_method == "sphinx":
            self.window.srmenu.entryconfigure(0, label="Sphinx")
        elif self.trainer.speech_recognition_method == "google":
            self.srmenu.entryconfigure(1, label="Google")
        # Add checkmark to newly selected speech recognition method
        if sr_meth == "sphinx":
            self.window.srmenu.entryconfigure(0, label="Sphinx " + "\u2713")
        elif sr_meth == "google":
            self.srmenu.entryconfigure(1, label="Google " + "\u2713")
        # Update speech recognition method
        self.trainer.speech_recognition_method = sr_meth
        self.ulog(f"Switching to {sr_meth} speech recognition")


def main():
    """Run the pronunciation trainer app"""
    root = tk.Tk()
    App(root, lang="en-US")
    root.mainloop()


if __name__ == "__main__":
    main()
