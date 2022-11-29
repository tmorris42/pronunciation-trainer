"""The MenuBar Component"""
from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING

from pronunciation_trainer.definitions.sr_methods import SrMethod

from .advanced_menu import AdvancedMenu
from .file_menu import FileMenu
from .language_menu import LanguageMenu

if TYPE_CHECKING:
    from pronunciation_trainer.components.main_frame import MainFrame


class MenuBar(tk.Menu):
    """The MenuBar Component"""

    def __init__(self, master: MainFrame):
        super().__init__(master)
        self.master: MainFrame = master

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

    def change_sr(self, sr_engine: SrMethod):
        """Propagate event"""
        self.master.change_sr(sr_engine)
