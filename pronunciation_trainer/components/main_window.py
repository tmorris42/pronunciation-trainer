"""The top level window for the GUI"""
import tkinter as tk
from tkinter import filedialog

from ..trainer import Trainer
from .main_frame import MainFrame
from .menus.menu_bar import MenuBar
from .phrasebook_frame import PhrasebookFrame
from .studio_frame import StudioFrame

LESSON_PATH = "lessons"


class MainWindow(tk.Tk):
    """Main window for the pronunciation trainer"""

    def __init__(
        self,
        app,
        trainer: Trainer,
    ):
        super().__init__()
        self.title("Pronunciation Trainer")
        self.app = app
        self.trainer = trainer
        self.target = tk.StringVar()
        self.log = tk.StringVar(value="loading...")

        main_frame = MainFrame(self)
        main_frame.pack(side=tk.TOP, fill=tk.X, expand=0)

        log_display = tk.Label(self, textvariable=self.log)
        log_display.pack(side=tk.TOP, fill=tk.BOTH, expand=0)

        # Create the menu bar
        self.filebar = MenuBar(main_frame)
        self.config(menu=self.filebar)

        # Create the Main Interactive Area
        self.studio_frame = StudioFrame(main_frame)
        self.studio_frame.pack(side=tk.LEFT, fill=tk.Y)

        phrasebook_frame = PhrasebookFrame(main_frame)
        phrasebook_frame.pack(side=tk.LEFT, fill=tk.X, expand=1)

        # Create and populate the phrases list
        self.phrases = phrasebook_frame.phrases

    def ulog(self, message):
        """Log a message to the info box"""
        self.log.set(message)

    def select_phraselist(self):
        """Open the file dialog to select a phrase list"""
        file = filedialog.askopenfile(
            parent=self,
            initialdir=LESSON_PATH,
            mode="rb",
            title="Open Lesson...",
        )
        if file is not None:
            self.load_phraselist(file)

    def select_phrase(self, *_, **__):
        """Select a word from the phrase list"""
        self.studio_frame.target_viewer.config(readonlybackground="white")
        target_position = self.phrases.curselection()
        self.target.set(self.phrases.get(target_position))

    def load_phraselist(self, phraselist=None):
        """Load a list of phrase for pronunciation practice"""
        if phraselist is not None:
            self.trainer.load_phrases(phraselist)
        self.phrases.delete(0, tk.END)
        for key in self.trainer.phrases:
            self.phrases.insert(tk.END, key)
        self.phrases.select_set(0)
        self.target.set(self.phrases.get(0))
        self.ulog(f"Loaded {self.trainer.phrase_dictionary['__PACKNAME__']}")

    def change_sr(self, sr_meth):
        """Change speech recognition method and update menus"""
        # Remove checkmark from previously selected speech recognitiongg method
        if self.trainer.speech_recognition_method == "sphinx":
            self.filebar.advanced_menu.sr_menu.entryconfigure(
                0, label="Sphinx"
            )
        elif self.trainer.speech_recognition_method == "google":
            self.filebar.advanced_menu.sr_menu.entryconfigure(
                1, label="Google"
            )
        # Add checkmark to newly selected speech recognition method
        if sr_meth == "sphinx":
            self.filebar.advanced_menu.sr_menu.entryconfigure(
                0, label="Sphinx " + "\u2713"
            )
        elif sr_meth == "google":
            self.filebar.advanced_menu.sr_menu.entryconfigure(
                1, label="Google " + "\u2713"
            )
        # Update speech recognition method
        self.trainer.speech_recognition_method = sr_meth
        self.ulog(f"Switching to {sr_meth} speech recognition")

    def change_language(self, lang="en-US"):
        """Change speech recognition language and update menus"""
        # Remove checkmark from previously selected language
        if self.trainer.language == "en-US":
            self.filebar.language_menu.entryconfigure(0, label="English")
        elif self.trainer.language == "fr-FR":
            self.filebar.language_menu.entryconfigure(1, label="French")
        # Add checkmark to newly selected language
        if lang == "en-US":
            self.filebar.language_menu.entryconfigure(
                0, label="English " + "\u2713"
            )
        elif lang == "fr-FR":
            self.filebar.language_menu.entryconfigure(
                1, label="French " + "\u2713"
            )

        self.trainer.language = lang
        self.ulog(f"Language changed to: {lang}")

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
            self.studio_frame.target_viewer.config(readonlybackground="green")
        else:
            self.ulog(f'I heard  "{response}"! Try again!')
            self.phrases.itemconfig(target_position, {"bg": "red"})
            self.studio_frame.target_viewer.config(readonlybackground="red")
