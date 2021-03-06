from random import randint
import pyttsx3
import os, sys
import calendar
import datetime
import time
import webbrowser
import tkinter as tk
import threading
import logging
import subprocess

try:
    from playsound import playsound
except ImportError as e:
    init_logging()
    init_packages()

import Window
import Listener

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
def init_logging():
    #Create and configure logger
    global logger
    if not os.path.exists(os.path.join("log")):
        os.makedirs("log")
    logfilename = "walterlog-"  + datetime.datetime.now().strftime("%I-%M%p-%d-%B-%Y")
    filepath = os.path.join("log", logfilename + ".log")
    logging.basicConfig(filename=filepath,
                        format='%(asctime)s %(levelname)s : %(message)s',
                        filemode='a+')

    logger=logging.getLogger()
    logger.setLevel(logging.DEBUG)

def init_packages():
    # Add check for python 3.6
    if sys.version_info.major != 3 and sys.version_info.minor != 6:
        logger.error("Python version required 3.6 but found " + sys.version_info.major + "." + sys.version_info.minor)
        logger.debug("PyAudio package doesn't have support for python version > 3.6")
        os._exit(0)

    # Add check for dependent modules
    try:
        import pip
        reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
        installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

        required_pkgs = ['pyttsx3', 'playsound', 'pillow', 'pyaudio']
        for pkg in required_pkgs:
            if pkg not in [x.lower() for x in installed_packages]:
                print(pkg)
                logger.debug(pkg + "is not installed in the system.")
                install(pkg)
    except ImportError as e:
        logger.error("pip is not installed. Please install pip to continue.")
        logger.debug(str(e))
        os.exit(0)

def install(package):
    logger.debug("Installing package " + package)
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

class Assistant(threading.Thread):
    """docstring for Assistant"""
    def __init__(self):
        self.abusive = ["bitch", "fuck", "asshole", "fucker", "motherfucker"]
        self.listener = Listener.Listener()

        threading.Thread.__init__(self)
        self.start()

    def quitWindow(self, root):
        root.destroy()
        logger.info("Destroying window.")
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
        self.walterlabel = tk.Label(root, textvariable=labelText2, fg='white', bg='#1c1b1b', pady=20, font=("Courier", 20), wraplength=800)
        self.userlabel.pack()
        self.walterlabel.pack()

        self.window = Window.Window(root)
        self.window.pack()
        self.window.load("siri.gif")
        self.window.mainloop()

    def process(self, data):
        logger.debug("Processing " + data)
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
            os._exit(0)

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

        time.sleep(1)
        self.speak(welcomeText)
        while True:
            try:
                data = ""
                logger.debug("Listening...")
                data = self.listener.listen()

                if data == -1 or data == -2:
                    logger.debug("Failed to understand the voice")
                    continue

                labelText = tk.StringVar()
                labelText.set(data)
                self.userlabel.config(textvariable=labelText)

                self.process(data)
            except KeyboardInterrupt as e:
                logger.info("You pressed <ESC>. Exiting...")
                os._exit(0)
            except Exception as e:
                logger.error("Exception occured")
                logger.error(str(e))
                labelText = tk.StringVar()
                labelText.set("Opps! Exception alert. Check terminal.")
                self.userlabel.config(textvariable=labelText)

    def speak(self, message):
        logger.debug("Speaking: " + message)
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
        logger.debug("Searching for directory: " + folderName)

        flag = 0
        while(len(spaths) > 0):
            currentPath = spaths[0]
            logger.debug("Searching: " + currentPath)
            root, dirs, _ = next(os.walk(currentPath))

            for dir in dirs:
                if folderName.lower() == str(dir).lower():
                    speak("There you go.")
                    logger.debug("Found: " + str(dir) + " @ " + str(root))
                    flag = 1

                    # To open the explorer
                    pathToOpen = os.path.join(root, str(dir))
                    logger.debug("Opening path in window: " + pathToOpen)
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
            logger.debug("Directory not found: " + folderName)
            speak("Sorry, specified directory not found.")

if __name__ == '__main__':
    init_logging()
    init_packages()

    assitant = Assistant()
    assitant.main()
