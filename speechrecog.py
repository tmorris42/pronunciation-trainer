#!/usr/bin/env python3

#### TODO:
##add mp3/wav playback of what word SHOULD sound like
##?? add playback of what you sound like? maybe?
##create separate lessons

import speech_recognition as sr
from pprint import pprint
import tkinter as tk
import io

LESSON_PATH = 'C:\\Users\\HeeHe\\Documents\\_THM\\_VirtualBox\\CinnaMint\\Code\\Python\\Language App\\lessons\\'

def check_sphinx(audio,lang='en-US'):
    # recognize speech using Sphinx
    r = sr.Recognizer()
    try:
        text = r.recognize_sphinx(audio,language=lang)
        print("Sphinx thinks you said \"" + text +"\" "+ str(type(text)))
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
        print("Google Speech Recognition thinks you said: {}".format(text['alternative'][0]['transcript']))
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
        self.master = master
        
        self.make_window()
        self.load_phraselist(self.phrase_pack)

    def ulog(self, message, flag=None):
        self.log.set(message)

    def make_window(self):
        self.master.winfo_toplevel().title("Say it")

        self.filebar = tk.Menu(self.master)
        
        self.main = tk.Frame(self.master)
        self.console = tk.Label(self.master, textvariable=self.log)
##        self.filebar.pack(side=tk.TOP,fill=tk.X)
        self.main.pack(side=tk.TOP,fill=tk.X,expand=0)
        self.console.pack(side=tk.TOP,fill=tk.BOTH,expand=0)
        
        self.filemenu = tk.Menu(self.filebar,tearoff=0)
        self.filemenu.add_command(label="Open", command=self.select_phraselist)
        self.filemenu.add_command(label="Quit", command=self.master.destroy)
        self.filebar.add_cascade(label="File", menu=self.filemenu)
        self.langmenu = tk.Menu(self.filebar,tearoff=0)
        self.langmenu.add_command(label="English", command=lambda:self.change_language('en-US'))
        self.langmenu.add_command(label="French", command=lambda:self.change_language('fr-FR'))
        self.filebar.add_cascade(label="Language", menu=self.langmenu)
        self.advmenu = tk.Menu(self.filebar,tearoff=0)
        self.srmenu = tk.Menu(self.advmenu,tearoff=0)
        self.srmenu.add_command(label="Sphinx",command=lambda:self.change_sr('sphinx'))
        self.srmenu.add_command(label="Google",command=lambda:self.change_sr('google'))
        self.advmenu.add_cascade(label="Speech Recognition", menu=self.srmenu)
        self.filebar.add_cascade(label="Advanced", menu=self.advmenu)
        
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

        self.phrases.bind("<Double-Button-1>", self.select_phrase)
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
            print('whoops, try again, say "{0}" {1}'.format(target.encode(),type(target)))
            self.ulog('Whoops! Try again!')
            self.phrases.itemconfig(self.target_position, {'bg':'red'})
            self.targetViewer.config(readonlybackground='red')
            
    def change_sr(self, sr):
        self.sr_meth = sr
        self.ulog('Switching to {} speech recognition'.format(self.sr_meth))
        
    def select_phraselist(self):
        file = tk.filedialog.askopenfile(parent=self.master,initialdir=LESSON_PATH+self.lang,mode='rb',title='Open Lesson...')
        if file != None:
            self.load_phraselist(file)
        
    def load_phraselist(self,listname="test"):
        phrases=[]
        if type(listname) == io.BufferedReader:
            try:
                data = listname.read().decode('latin1')
            except UnicodeDecodeError as e:
                print(type(listname.read()))
                data = str(listname.read())
                print(data,type(data))
##                raise e
##            except IndexError as e:
##                raise e
            file=data.split('\n')            
            for line in file:
                nline=line.rstrip('\n')
                nline=line.rstrip('\r')                
                phrases.append(nline)
        else:
            self.ulog('Loading {}'.format(self.lang+"\\"+listname))
            try:
                with open(LESSON_PATH+self.lang+"\\"+listname) as file:
                    for line in file:
                        nline=line.rstrip('\n')
                        phrases.append(nline)                
            except FileNotFoundError:
                print('Language File Not Found')
                self.ulog('Error loading {}; loading default pack'.format(listname))
                phrases = ['default package','hello','fine','what\'s up','merci','oui','non']
        packname, phrases = phrases[0], phrases[1:]
        self.phrases.delete(0,tk.END)
        for word in phrases:
            self.phrases.insert(tk.END, word)
        self.phrases.select_set(0)
        self.target.set(self.phrases.get(0))
        self.ulog('Loaded {}'.format(packname))
        
    def select_language(self):
        tk.messagebox.askquestion('Select Language','French or English?')

    def change_language(self,lang='en-US'):
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
