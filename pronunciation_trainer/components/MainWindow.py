import tkinter as tk
from tkinter import filedialog

LESSON_PATH = "lessons"

class MainWindow:
    """Main window for the pronunciation trainer"""
    def __init__(self, master, listen_callback, speak_callback):
        self.target = tk.StringVar()
        self.master = master
        self.log = tk.StringVar(value="loading...")

        self.master.winfo_toplevel().title("Pronunciation Trainer")
        main_frame = tk.Frame(self.master)
        log_display = tk.Label(self.master, textvariable=self.log)
        main_frame.pack(side=tk.TOP, fill=tk.X, expand=0)
        log_display.pack(side=tk.TOP, fill=tk.BOTH, expand=0)
        # Create the menu bar
        filebar = tk.Menu(self.master)
        filemenu = tk.Menu(filebar, tearoff=0)
        filemenu.add_command(label="Open", command=self.select_phraselist)
        filemenu.add_command(label="Quit", command=self.master.destroy)
        filebar.add_cascade(label="File", menu=filemenu)
        self.langmenu = tk.Menu(filebar, tearoff=0)
        self.langmenu.add_command(
            label="English", command=lambda: self.change_language("en-US")
        )
        self.langmenu.add_command(
            label="French", command=lambda: self.change_language("fr-FR")
        )
        filebar.add_cascade(label="Language", menu=self.langmenu)
        advanced_menu = tk.Menu(filebar, tearoff=0)
        self.srmenu = tk.Menu(advanced_menu, tearoff=0)
        self.srmenu.add_command(
            label="Sphinx", command=lambda: self.change_sr("sphinx")
        )
        self.srmenu.add_command(
            label="Google", command=lambda: self.change_sr("google")
        )
        advanced_menu.add_cascade(label="Speech Recognition", menu=self.srmenu)
        filebar.add_cascade(label="Advanced", menu=advanced_menu)
        self.master.config(menu=filebar)
        # Create the Main Interactive Area
        studio_frame = tk.Frame(main_frame)
        phrasebook_frame = tk.Frame(main_frame)
        studio_frame.pack(side=tk.LEFT, fill=tk.Y)
        phrasebook_frame.pack(side=tk.LEFT, fill=tk.X, expand=1)
        # Create the buttons and display for the Main Interactive Area
        listen_button = tk.Button(
            studio_frame, text="Listen", width=25, command=listen_callback
        )
        speak_button = tk.Button(
            studio_frame, text="Speak", width=25, command=speak_callback
        )
        self.target_viewer = tk.Entry(
            studio_frame,
            textvariable=self.target,
            justify=tk.CENTER,
            state="readonly",
            readonlybackground="white",
        )
        listen_button.pack(side=tk.TOP)
        speak_button.pack(side=tk.TOP)
        self.target_viewer.pack(side=tk.TOP)
        # Create and populate the phrases list
        self.phrases = tk.Listbox(phrasebook_frame)
        self.phrases.bind("<Double-Button-1>", self.select_phrase)
        self.phrasescroll = tk.Scrollbar(phrasebook_frame)
        self.phrases.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.phrasescroll.pack(side=tk.LEFT, fill=tk.Y)
        self.phrases.config(yscrollcommand=self.phrasescroll.set)
        self.phrasescroll.config(command=self.phrases.yview)


    def select_phraselist(self):
        """Open the file dialog to select a phrase list"""
        file = filedialog.askopenfile(
            parent=self.master,
            initialdir=LESSON_PATH + self.trainer.language,
            mode="rb",
            title="Open Lesson...",
        )
        if file is not None:
            self.load_phraselist(file)

    def select_phrase(self, *_, **__):
        """Select a word from the phrase list"""
        self.target_viewer.config(readonlybackground="white")
        target_position = self.phrases.curselection()
        self.target.set(self.phrases.get(target_position))

    
