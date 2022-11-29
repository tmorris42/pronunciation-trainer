"""The File Menu Component"""
import tkinter as tk


class FileMenu(tk.Menu):
    """The File Menu Component"""

    def __init__(self, master):
        super().__init__(master, tearoff=0)
        self.master = master
        self.add_command(label="Open", command=master.select_phraselist)
        self.add_command(label="Quit", command=master.destroy)
