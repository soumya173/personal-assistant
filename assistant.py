from random import randint
import pyttsx3
import os
import calendar
import datetime
import time
import webbrowser
from playsound import playsound
import tkinter as tk
import threading
import keyboard

import Window
import Listener

# from time import ctime

######################################################
# Module Installation guide
# ---------------------------------------------------
# pip install gTTS
# pip install pyttsx3
# pip install SpeechRecognition
# pip install playsound
# http://www.nirsoft.net/utils/nircmd.html - Download nirCmd to execute commands
# pip install chatterbot
# pip install pillow
######################################################

class Assistant(threading.Thread):
    """docstring for Assistant"""
    def __init__(self, name):
        self.abusive = ["bitch", "fuck", "asshole", "fucker", "motherfucker"]
        self.listener = Listener.Listener()

        threading.Thread.__init__(self)
        self.start()

    def run(self):
        root = tk.Tk()
        root.configure(background='#1c1b1b')
        root.bind('<Escape>', lambda e: root.destroy())

        # make it cover the entire screen
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.overrideredirect(1)
        root.geometry("%dx%d+0+0" % (w, h))

        labelText1 = tk.StringVar()
        labelText1.set("")

        labelText2 = tk.StringVar()
        self.label1 = tk.Label(root, textvariable=labelText1, fg='white', bg='#1c1b1b', pady=10, font=("Courier", 20), wraplength=800)
        self.label2 = tk.Label(root, textvariable=labelText2, fg='white', bg='#1c1b1b', pady=10, font=("Courier", 20), wraplength=800)
        self.label1.pack()
        self.label2.pack()

        window = Window.Window(root)
        window.pack()
        window.load("siri.gif")
        # label = tk.Label()
        window.mainloop()

    def process(self, data):
        #Cheks for abusive words
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
            site = "https://www." + data[startIndex:].lower() + ".com"
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
            data = ""
            data = self.listener.listen()
            labelText = tk.StringVar()
            labelText.set(data)
            self.label1.config(textvariable=labelText)

            if data == -1 or data == -2:
                # self.speak("Sorry, couldn't understand your voice.")
                continue

            self.process(data)

    def speak(self, message):
        labelText = tk.StringVar()
        labelText.set(message)
        self.label2.config(textvariable=labelText)

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

# abusive = ["bitch", "fuck", "asshole", "fucker", "motherfucker"]

# def speak(self, message):
#     engine = pyttsx3.init()
#     engine.say(message)
#     engine.setProperty('volume',0.9)
#     engine.runAndWait()

# def process(data):
#     #Cheks for abusive words
#     words = data.split(" ")

#     # if words in (x for x in abusive)
#     for word in words:
#         if word in abusive:
#             speak("Please do not use abusive words")
#             break

#     if "hello" == data or "hey" == data or "hi" == data:
#         greetings = ["Hey! How can I help you?", "Hello there.", "Hi!"]
#         greet = greetings[randint(0, len(greetings)-1)]
#         speak(greet)

#     if "say my name" in data:
#         speak("Heisenberg.")

#     if "you are stupid" in data:
#         speak("Sorry, if I made some mistake. I won't disappoint you next time.")

#     if "who are you" == data:
#         speak("I am a Personal Assistant designed by Mr. Heisenberg. I am here to make things easy for you.")

#     if "can you hear me" == data:
#         speak("Yes, I can hear you.")

#     if "you are awesome" == data:
#         speak("You are awesome too, bro.")

#     if "I love you" == data:
#         speak("Sorry, I have a boyfriend.")

#     if "tell me the time" == data:
#         now = datetime.datetime.now()
#         currentTime = "The time is "+str(now.hour)+" hour and "+str(now.minute)+" minute"
#         speak(currentTime)

#     if "show me the calendar" in data:
#         now = datetime.datetime.now()
#         year = now.year
#         month = now.month
#         cal = calendar.month(year, month)
#         speak("Here is the calendar.")
#         print(cal)

#     if data.lower().startswith("open"):
#         startIndex = len("open ")
#         site = "https://www." + data[startIndex:].lower() + ".com"
#         speak("There you go.")
#         webbrowser.open_new_tab(site)

#     if data.lower().startswith("google"):
#         #Codes to search google
#         startIndex = len("google ")
#         query = "https://www.google.co.in/search?q=" + data[startIndex:]
#         webbrowser.open_new_tab(query)

#     if "search folder" in data.lower():
#         searchFolder()

#     if "shutdown the PC" in data:
#         #Codes to shutdown
#         speak("Shutting down.")
#         # os.system("poweroff")
#         os.system('shutdown -s')

#     if "restart the PC" in data:
#         #Codes to restart
#         speak("Restarting.")
#         os.system("restart")

#     if "lock the PC" in data:
#         #Codes to lock the pc
#         speak("Locking the PC.")
#         os.popen('gnome-screensaver-command --lock')

#     if "take rest" in data:
#         speak("Okay. See you next time.")
#         exit()

#     if "mute the pc" in data.lower():
#         #Codes to mute the sound
#         # os.system("amixer set Master mute")
#         os.system("nircmd.exe mutesysvolume 1")

#     if "unmute" in data.lower():
#         # os.system("amixer set Master unmute")
#         os.system("nircmd.exe mutesysvolume 0")
#         speak("Done.")

#     if "toggle sound" in data.lower():
#         os.system("amixer set Master toggle")
#         speak("Done.")


#     if "run application" in data.lower():
#         print("App Name:")
#         appName = listenToMe()
#         try:
#             speak("There you go.")
#             os.system(appName.lower())
#         except Exception:
#             print("Sorry, something went wrong.")

#     # if data.lower().startswith("where is"):
#     #     mapUrl = data[10:]


# # Search for a folder
# def searchFolder():
#     speak("Okay, tell me the name of the folder.")

#     # Home directories
#     # spaths = [r"/home/soumya/", r"/media/soumya/Docs/", r"/media/soumya/Entertainment/"]
#     spaths= [r"E:\\"]

#     folderName = listenToMe()
#     folderName = folderName.lower()
#     speak("Searching, Please wait.")
#     print("Searching...")

#     flag = 0
#     while(len(spaths) > 0):
#         currentPath = spaths[0]
#         print("Currently searching: "+currentPath)
#         root, dirs, _ = next(os.walk(currentPath))


#         for dir in dirs:
#             if folderName.lower() == str(dir).lower():
#                 speak("There you go.")
#                 print("Found: " + str(dir) + " @ " + str(root))
#                 flag = 1

#                 # To open the explorer
#                 pathToOpen = os.path.join(root, str(dir))
#                 webbrowser.open(pathToOpen)
#                 break

#         # To prevent finding more places
#         if flag == 1:
#             break

#         spaths.remove(currentPath)

#         # Add other directories to the list
#         for dir in dirs:
#             if str(dir).startswith("."):
#                 continue
#             pathToAppend = os.path.join(root, dir)
#             spaths.append(pathToAppend)

#     if flag == 0:
#         speak("Sorry, specified directory not found.")

# listener = Listener.Listener()
# d = listener.listen()
# print(d)

# root = tk.Tk()
# lbl = Window.Window(root)
# lbl.pack()
# lbl.load('siri.gif')
# root.mainloop()

# welcomeText = "Hello! How can I help you?"

# time.sleep(2)
# speak(welcomeText)
# while 1:
#     data = ""
#     data = listenToMe()
#     process(data)