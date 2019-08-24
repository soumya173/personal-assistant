from random import randint
import pyttsx3
import os, sys
import calendar
import datetime
import time
import webbrowser
from playsound import playsound
import tkinter as tk
import threading
# import keyboard

import Window
import Listener

# from time import ctime

######################################################
# Module Installation guide
# ---------------------------------------------------
# Use Python 3.6 because Python 3.7 does not have support for PyAudio
# pip install gTTS (Not used now)
# pip install pyttsx3
# pip install SpeechRecognition
# pip install playsound
# http://www.nirsoft.net/utils/nircmd.html - Download nirCmd to execute commands
# pip install chatterbot (Not used. Not implemented yet)
# pip install pillow
######################################################

class Assistant(threading.Thread):
    """docstring for Assistant"""
    def __init__(self, name):
        self.abusive = ["bitch", "fuck", "asshole", "fucker", "motherfucker"]
        self.listener = Listener.Listener()

        threading.Thread.__init__(self)
        self.start()

    def quitWindow(self, root):
        root.destroy()
        print("Window Destroyed.")
        os._exit(0)

    def run(self):
        root = tk.Tk()
        root.configure(background='#1c1b1b')
        # root.bind('<Escape>', lambda e: root.destroy())
        root.bind('<Escape>', lambda e: self.quitWindow(root))

        # make it cover the entire screen
        # w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        # root.overrideredirect(1)
        # root.geometry("%dx%d+0+0" % (w-3, h-3))

        # root.attributes("-fullscreen", True)
        root.state("zoomed")

        labelText1 = tk.StringVar()
        labelText1.set("")

        labelText2 = tk.StringVar()
        self.userlabel = tk.Label(root, textvariable=labelText1, fg='white', bg='#1c1b1b', pady=10, font=("Courier", 20), wraplength=800)
        self.walterlabel = tk.Label(root, textvariable=labelText2, fg='white', bg='#1c1b1b', pady=10, font=("Courier", 20), wraplength=800)
        self.userlabel.pack()
        self.walterlabel.pack()

        self.window = Window.Window(root)
        self.window.pack()
        self.window.load("siri.gif")
        # label = tk.Label()
        self.window.mainloop()

    def process(self, data):
        #Checks for abusive words
        words = data.split(" ")

        # if words in (x for x in abusive)
        for word in words:
            if word in self.abusive:
                self.speak("Please do not use abusive words")
                break

        if "hello" == data or "hey" == data or "hi" == data:
            greetings = ["Hey! How can I help you?", "Hello there.", "Hi!"]
            greet = greetings[randint(0, len(greetings)-1)]
            self.speak(greet)

        if "say my name" in data:
            self.speak("Heisenberg.")

        if "you are stupid" in data:
            self.speak("Sorry, if I made some mistake. I won't disappoint you next time.")

        if "who are you" == data:
            self.speak("My name is Walter, a Personal Assistant designed by Mr. Heisenberg. I am here to make things easy for you.")

        if "what you can do" == data:
            self.speak("I can do a couple of things right now. Like, google something, open some website, shutdown or restart or lock the PC and some other things.")

        if "can you hear me" == data:
            self.speak("Yes, I can hear you.")

        if "you are awesome" == data:
            self.speak("You are awesome too, bro.")

        if "are you there" == data:
            self.speak("Yes, I'm listening.")

        if "tell me the time" == data:
            now = datetime.datetime.now()
            currentTime = "The time is "+str(now.hour)+" hour and "+str(now.minute)+" minute"
            self.speak(currentTime)

        if "show me the calendar" in data:
            now = datetime.datetime.now()
            year = now.year
            month = now.month
            cal = calendar.month(year, month)
            self.speak("Here is the calendar.")
            print(cal)

        if data.lower().startswith("open"):
            startIndex = len("open ")
            domain = data[startIndex:].lower()
            domain.replace(" ", "")
            site = "https://www." + domain + ".com"
            self.speak("There you go.")
            webbrowser.open_new_tab(site)

        if data.lower().startswith("google"):
            #Codes to search google
            startIndex = len("google ")
            query = "https://www.google.co.in/search?q=" + data[startIndex:]
            self.speak("There you go.")
            webbrowser.open_new_tab(query)

        if "search folder" in data.lower():
            searchFolder()

        if "shutdown the PC" in data:
            #Codes to shutdown
            self.speak("Shutting down.")
            # os.system("poweroff")
            os.system('shutdown -s')

        if "restart the PC" in data:
            #Codes to restart
            self.speak("Restarting.")
            os.system("restart")

        if "lock the PC" in data:
            #Codes to lock the pc
            self.speak("Locking the PC.")
            os.popen('gnome-screensaver-command --lock')

        if "take rest" in data:
            self.speak("Okay. See you next time.")
            exit()

        if "mute the pc" in data.lower():
            #Codes to mute the sound
            # os.system("amixer set Master mute")
            self.speak("As your wish but I'll be unable to speak to you.")
            os.system("nircmd.exe mutesysvolume 1")

        if "unmute" in data.lower():
            # os.system("amixer set Master unmute")
            os.system("nircmd.exe mutesysvolume 0")
            self.speak("Done.")

        if "toggle sound" in data.lower():
            self.speak("Done.")
            os.system("nircmd.exe mutesysvolume 2")

    def main(self):
        welcomeText = "Hello! How can I help you?"

        time.sleep(2)
        self.speak(welcomeText)
        while True:
            try:
                data = ""
                data = self.listener.listen()

                if data == -1 or data == -2:
                    # self.speak("Sorry, couldn't understand your voice.")
                    continue

                labelText = tk.StringVar()
                labelText.set(data)
                self.userlabel.config(textvariable=labelText)

                self.process(data)
            except KeyboardInterrupt as e:
                print("Exiting...")
                os._exit(0)
            except Exception as e:
            	labelText = tk.StringVar()
            	labelText.set("Opps! Exception alert. Check terminal.")
            	self.userlabel.config(textvariable=labelText)

    def speak(self, message):
        labelText = tk.StringVar()
        labelText.set(message)
        self.walterlabel.config(textvariable=labelText)

        engine = pyttsx3.init()
        engine.say(message)
        engine.setProperty('volume',0.9)
        engine.runAndWait()

    # # Search for a folder
    def searchFolder(self):
        speak("Okay, tell me the name of the folder.")

        # Home directories
        # spaths = [r"/home/soumya/", r"/media/soumya/Docs/", r"/media/soumya/Entertainment/"]
        spaths= [r"E:\\"]

        folderName = listenToMe()
        folderName = folderName.lower()
        speak("Searching, Please wait.")
        print("Searching...")

        flag = 0
        while(len(spaths) > 0):
            currentPath = spaths[0]
            print("Currently searching: "+currentPath)
            root, dirs, _ = next(os.walk(currentPath))


            for dir in dirs:
                if folderName.lower() == str(dir).lower():
                    speak("There you go.")
                    print("Found: " + str(dir) + " @ " + str(root))
                    flag = 1

                    # To open the explorer
                    pathToOpen = os.path.join(root, str(dir))
                    webbrowser.open(pathToOpen)
                    break

            # To prevent finding more places
            if flag == 1:
                break

            spaths.remove(currentPath)

            # Add other directories to the list
            for dir in dirs:
                if str(dir).startswith("."):
                    continue
                pathToAppend = os.path.join(root, dir)
                spaths.append(pathToAppend)

        if flag == 0:
            speak("Sorry, specified directory not found.")


if __name__ == '__main__':
    # root = tk.Tk()
    # window = Window.Window(root)
    # # window.setVars("siri.gif")
    # window.pack()
    # window.load("siri.gif")
    # window.mainloop()

    assitant = Assistant("siri.gif")
    assitant.main()
