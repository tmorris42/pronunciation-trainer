"""The Speech Recognition Menu Component"""
import tkinter as tk

from pronunciation_trainer.definitions.sr_methods import SrMethod


class SRMenu(tk.Menu):
    """The Speech Recognition Menu Component"""

    def __init__(self, master):
        super().__init__(master, tearoff=0)
        self.add_command(
            label="Sphinx", command=lambda: master.change_sr(SrMethod.SPHINX)
        )
        self.add_command(
            label="Google", command=lambda: master.change_sr(SrMethod.GOOGLE)
        )
