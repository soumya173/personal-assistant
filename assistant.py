from gtts import gTTS
import speech_recognition as sr
import os
import calendar
import datetime
import time
import webbrowser
from random import randint
# from time import ctime

abusive = ["bitch", "fuck", "asshole", "fucker", "motherfucker"]

def speak(message):
    tts = gTTS(text=message, lang='en')
    try:
        tts.save("pcvoice.mp3")
    except Exception:
        print("Couldn't save the audio file.")


    # this is for linux
    os.system("mpg321 pcvoice.mp3")

def listenToMe():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration = 1)
        print("Say something!")
        audio = r.listen(source)

        # Speech recognition using Google Speech Recognition
        data = ""
        try:
            # Uses the default API key
            # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            data = r.recognize_google(audio)
            print("You said: " + data)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            speak("Sorry, I can't understand you.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return data

def process(data):
    #Cheks for abusive words
    words = data.split(" ")

    # if words in (x for x in abusive)
    for word in words:
        if word in abusive:
            speak("Please do not use abusive words")
            break

    if "hello" == data or "hey" == data or "hi" == data:
        greetings = ["Hey! How can I help you?", "Hello there.", "Hi!"]
        greet = greetings[randint(0, len(greetings)-1)]
        speak(greet)

    if "say my name" in data:
        speak("Heisenberg.")

    if "you are stupid" in data:
        speak("Sorry, if I made some mistake. I won't disappoint you next time.")

    if "who are you" == data:
        speak("I am a Personal Assistant designed by Mr. Heisenberg. I am here to make things easy for you.")

    if "can you hear me" == data:
        speak("Yes, I can hear you.")

    if "you are awesome" == data:
        speak("You are awesome too, bro.")

    if "I love you" == data:
        speak("Sorry, I have a boyfriend.")

    if "tell me the time" == data:
        now = datetime.datetime.now()
        currentTime = "The time is "+str(now.hour)+" hour and "+str(now.minute)+" minute"
        speak(currentTime)

    if "show me the calendar" in data:
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        cal = calendar.month(year, month)
        speak("Here is the calendar.")
        print(cal)

    if data.lower().startswith("open"):
        startIndex = len("open ")
        site = "https://www." + data[startIndex:].lower() + ".com"
        speak("There you go.")
        webbrowser.open_new_tab(site)

    if data.lower().startswith("google"):
        #Codes to search google
        startIndex = len("google ")
        query = "https://www.google.co.in/search?q=" + data[startIndex:]
        webbrowser.open_new_tab(query)

    if "search folder" in data.lower():
        searchFolder()

    if "shutdown the PC" in data:
        #Codes to shutdown
        speak("Shutting down.")
        os.system("poweroff")

    if "restart the PC" in data:
        #Codes to restart
        speak("Restarting.")
        os.system("restart")

    if "lock the PC" in data:
        #Codes to lock the pc
        speak("Locking the PC.")
        os.popen('gnome-screensaver-command --lock')

    if "take rest" in data:
        speak("Okay. See you next time.")
        exit()

    if "mute the pc" in data.lower():
        #Codes to mute the sound
        os.system("amixer set Master mute")

    if "unmute" in data.lower():
        os.system("amixer set Master unmute")
        speak("Done.")

    if "toggle sound" in data.lower():
        os.system("amixer set Master toggle")
        speak("Done.")


    if "run application" in data.lower():
        print("App Name:")
        appName = listenToMe()
        try:
            speak("There you go.")
            os.system(appName.lower())
        except Exception:
            print("Sorry, something went wrong.")

    # if data.lower().startswith("where is"):
    #     mapUrl = data[10:]


# Search for a folder
def searchFolder():
    speak("Okay, tell me the name of the folder.")

    # Home directories
    spaths = [r"/home/soumya/", r"/media/soumya/Docs/", r"/media/soumya/Entertainment/"]

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


welcomeText = "Hello! How can I help you?"

time.sleep(2)
speak(welcomeText)
while 1:
    data = ""
    data = listenToMe()
    process(data)
