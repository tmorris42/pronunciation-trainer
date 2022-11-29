"""Frame containing the phrase list"""
import tkinter as tk


class PhrasebookFrame(tk.Frame):
    """Frame containing the phrase list"""

    def __init__(self, master):
        super().__init__(master)
        self.phrases = tk.Listbox(self)
        self.phrases.bind("<Double-Button-1>", master.select_phrase)
        self.phrasescroll = tk.Scrollbar(self)
        self.phrases.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.phrasescroll.pack(side=tk.LEFT, fill=tk.Y)
        self.phrases.config(yscrollcommand=self.phrasescroll.set)
        self.phrasescroll.config(command=self.phrases.yview)
