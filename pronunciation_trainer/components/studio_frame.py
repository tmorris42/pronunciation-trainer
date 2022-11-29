"""Frame containing the listen and speak buttons"""
import tkinter as tk


class StudioFrame(tk.Frame):
    """Frame containing the listen and speak buttons"""

    def __init__(self, master):
        super().__init__(master)
        # Create the buttons and display for the Main Interactive Area
        listen_button = tk.Button(
            self, text="Listen", width=25, command=master.play_example
        )
        speak_button = tk.Button(
            self, text="Speak", width=25, command=master.speak
        )
        self.target_viewer = tk.Entry(
            self,
            textvariable=master.target,
            justify=tk.CENTER,
            state="readonly",
            readonlybackground="white",
        )
        listen_button.pack(side=tk.TOP)
        speak_button.pack(side=tk.TOP)
        self.target_viewer.pack(side=tk.TOP)
