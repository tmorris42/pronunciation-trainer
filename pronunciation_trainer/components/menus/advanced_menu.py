"""The Advanced Menu Component"""
from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING

from pronunciation_trainer.definitions.sr_methods import SrMethod

from .sr_menu import SRMenu

if TYPE_CHECKING:
    from pronunciation_trainer.components.menus.menu_bar import MenuBar


class AdvancedMenu(tk.Menu):
    """The Advanced Menu Component"""

    def __init__(self, master: MenuBar):
        super().__init__(master, tearoff=0)
        self.master: MenuBar = master
        self.sr_menu = SRMenu(self)
        self.add_cascade(label="Speech Recognition", menu=self.sr_menu)

    def change_sr(self, sr_engine: SrMethod):
        """Propagate event"""
        self.master.change_sr(sr_engine)
