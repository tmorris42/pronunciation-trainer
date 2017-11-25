#!/usr/bin/env python3

#### TODO:
##add mp3/wav playback of what word SHOULD sound like
##?? add playback of what you sound like? maybe?
##add language selection dialog box
##add toggle for google/sphinx
##make filemenu work
##create separate lessons

import speech_recognition as sr
from pprint import pprint
import tkinter as tk

def check_sphinx(audio,lang='en-US'):
    # recognize speech using Sphinx
    r = sr.Recognizer()
    try:
        text = r.recognize_sphinx(audio,language=lang)
        print("Sphinx thinks you said \"" + text +"\"")
        return text
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    return None

def check_google(audio,lang='en-US'):
    # recognize speech using Google Speech Recognition
    r = sr.Recognizer()
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)
        text = r.recognize_google(audio, show_all=True,language="fr-FR")
        print("Google Speech Recognition thinks you said:")        
        pprint(text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return None

def get_audio():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    return audio

def fake_google():
    return {'final': True, 'alternative': [{'transcript': "s'il vous plaît", 'confidence': 0.85880154}, {'transcript': 'si vous plaît'}, {'transcript': 'si je me plais'}, {'transcript': 'il me plaît'}, {'transcript': 'si il me plaît'}]}

class App:
    def __init__(self, master,method='sphinx',lang='en-US',phrasepack='greetings.txt'):
        self.target = tk.StringVar()
        self.target_position = 0
        self.sr_meth = method
        self.lang = lang
        self.log = tk.StringVar(value='test')
        self.phrase_pack = phrasepack
        
        self.make_window(master)
        self.ulog('window loaded')
        self.load_phraselist(self.phrase_pack)
        self.phrases.select_set(0)
        self.target.set(self.phrases.get(self.phrases.curselection()))

    def ulog(self, message, flag=None):
        self.log.set(message)

    def make_window(self, master):
        self.master = master

        self.filebar = tk.Menu(self.master)
        
        self.main = tk.Frame(self.master)
        self.console = tk.Label(self.master, textvariable=self.log)
##        self.filebar.pack(side=tk.TOP,fill=tk.X)
        self.main.pack(side=tk.TOP,fill=tk.X,expand=0)
        self.console.pack(side=tk.TOP,fill=tk.BOTH,expand=0)
        
        self.filemenu = tk.Menu(self.filebar,tearoff=0)
        self.filemenu.add_command(label="Open", command=self.load_phraselist)
        self.filemenu.add_command(label="Quit", command=self.master.destroy)
        self.filebar.add_cascade(label="File", menu=self.filemenu)
##        self.file = tk.Menubutton(self.filebar,text="File")
##        self.edit = tk.Menubutton(self.filebar,text="Edit")
##        self.file.pack(side=tk.LEFT)
##        self.edit.pack(side=tk.LEFT)        

        self.menu = tk.Frame(self.main)
        self.studio = tk.Frame(self.main)
        self.phrasebook = tk.Frame(self.main)
        self.menu.pack(side=tk.LEFT,fill=tk.Y)
        self.studio.pack(side=tk.LEFT,fill=tk.Y)
        self.phrasebook.pack(side=tk.LEFT,fill=tk.X,expand=1)        
        
        self.selectLanguageButton = tk.Button(self.menu, text="Select Language", width=25, command=self.select_language)
        self.selectLanguageButton.pack(side=tk.TOP)

        self.listenButton = tk.Button(self.studio,text="Listen",width=25)
        self.speakButton = tk.Button(self.studio,text="Speak",width=25,command=self.speak)
        self.targetViewer = tk.Entry(self.studio, textvariable=self.target, justify=tk.CENTER,state="readonly",readonlybackground='white')
        self.listenButton.pack(side=tk.TOP)
        self.speakButton.pack(side=tk.TOP)
        self.targetViewer.pack(side=tk.TOP)

        self.phrases = tk.Listbox(self.phrasebook)
##        self.phrases.insert(tk.END,' ')
        
        
        self.phrases.bind("<Double-Button-1>", self.select_phrase)
##        self.phrases.config(selectbackground=None,selectborderwidth=0,selectforeground=None)
        self.phrasescroll = tk.Scrollbar(self.phrasebook)
        self.phrases.pack(side=tk.LEFT,fill=tk.X,expand=1)
        self.phrasescroll.pack(side=tk.LEFT,fill=tk.Y)
        self.phrases.config(yscrollcommand=self.phrasescroll.set)
        self.phrasescroll.config(command=self.phrases.yview)

        self.master.config(menu=self.filebar)

    def select_phrase(self, *args):
        self.targetViewer.config(readonlybackground='white')
        self.target_position=self.phrases.curselection()
        self.target.set(self.phrases.get(self.target_position))
        
##        self.speak()

    def speak(self, *args):
##        if args:
##            print(args[0].__dict__)
##        target = 'hello'
        target = self.target.get()
        audio = get_audio()
        if self.sr_meth == 'sphinx':
            result = check_sphinx(audio,lang=self.lang)
        elif self.sr_meth == 'google':
            result = check_google(audio,lang=self.lang)
            result = result['alternative'][0]['transcript']
        if result == target:
            print('you got it!')
            self.ulog('Good job!')
            self.phrases.itemconfig(self.target_position, {'bg':'green'})
            self.targetViewer.config(readonlybackground='green')
        else:
            print('whoops, try again, say "{0}"'.format(target))
            self.ulog('Whoops! Try again!')
            self.phrases.itemconfig(self.target_position, {'bg':'red'})
            self.targetViewer.config(readonlybackground='red')

    def load_phraselist(self,listname="test"):
        self.ulog('Loading {}'.format(listname))
        try:
            with open(listname) as file:
                phrases=[]
                for line in file:
                    nline=line.rstrip('\n')
                    phrases.append(nline)
        except FileNotFoundError:
            print('Language File Not Found')
            self.ulog('Error loading {}; loading default pack'.format(listname))
            phrases = ['hello','fine','what\'s up','merci','oui','non']

        for word in phrases:
            self.phrases.insert(tk.END, word)
        
        
    def select_language(self,lang='en-US'):
        self.lang = lang
        self.ulog('Language changed to: {}'.format(lang))

if __name__ == '__main__':    
##    audio = get_audio()
##    text = check_sphinx(audio)
##    text2 = check_google(audio)
##    text2 = fake_google()
##    pprint(text2)

    root = tk.Tk()
##    app = App(root,lang='fr-FR')
    app = App(root,lang='en-US')
    root.mainloop()
