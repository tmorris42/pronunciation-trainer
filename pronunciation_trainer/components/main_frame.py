"""The main frame"""
import tkinter as tk


class MainFrame(tk.Frame):
    """The main frame"""

    def __init__(self, master):
        super().__init__(master)
        self.target = master.target

    def play_example(self):
        """Propagate event"""
        self.master.play_example()

    def speak(self):
        """Propagate event"""
        self.master.speak()

    def select_phraselist(self):
        """Propagate event"""
        self.master.select_phraselist()

    def change_language(self, language):
        """Propagate event"""
        self.master.change_language(language)

    def change_sr(self, sr_engine):
        """Propagate event"""
        self.master.change_sr(sr_engine)

    def select_phrase(self, *args, **kwargs):
        """Propagate event"""
        self.master.select_phrase(args, kwargs)
