"""The Advanced Menu Component"""
import tkinter as tk

from .sr_menu import SRMenu


class AdvancedMenu(tk.Menu):
    """The Advanced Menu Component"""

    def __init__(self, master):
        super().__init__(master, tearoff=0)
        self.sr_menu = SRMenu(self)
        self.add_cascade(label="Speech Recognition", menu=self.sr_menu)

    def change_sr(self, sr_engine):
        """Propagate event"""
        self.master.change_sr(sr_engine)
