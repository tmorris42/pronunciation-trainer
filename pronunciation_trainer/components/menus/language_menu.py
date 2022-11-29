"""The Language Menu Component"""
import tkinter as tk


class LanguageMenu(tk.Menu):
    """The Language Menu Component"""

    def __init__(self, master):
        super().__init__(master, tearoff=0)
        self.add_command(
            label="English", command=lambda: master.change_language("en-US")
        )
        self.add_command(
            label="French", command=lambda: master.change_language("fr-FR")
        )
