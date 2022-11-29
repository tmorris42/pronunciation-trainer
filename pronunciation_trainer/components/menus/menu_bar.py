"""The MenuBar Component"""
import tkinter as tk

from .advanced_menu import AdvancedMenu
from .file_menu import FileMenu
from .language_menu import LanguageMenu


class MenuBar(tk.Menu):
    """The MenuBar Component"""

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        filemenu = FileMenu(self)
        self.add_cascade(label="File", menu=filemenu)

        self.language_menu = LanguageMenu(self)
        self.add_cascade(label="Language", menu=self.language_menu)

        self.advanced_menu = AdvancedMenu(self)
        self.add_cascade(label="Advanced", menu=self.advanced_menu)

    def select_phraselist(self):
        """Propagate event"""
        self.master.select_phraselist()

    def change_language(self, language):
        """Propagate event"""
        self.master.change_language(language)

    def change_sr(self, sr_engine):
        """Propagate event"""
        self.master.change_sr(sr_engine)
