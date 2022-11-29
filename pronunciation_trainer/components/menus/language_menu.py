"""The Language Menu Component"""
import tkinter as tk

from pronunciation_trainer.definitions.languages import Language


class LanguageMenu(tk.Menu):
    """The Language Menu Component"""

    def __init__(self, master):
        super().__init__(master, tearoff=0)
        self.add_command(
            label="English",
            command=lambda: master.change_language(Language.ENGLISH),
        )
        self.add_command(
            label="French",
            command=lambda: master.change_language(Language.FRENCH),
        )
