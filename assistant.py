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
import paramiko
import re
import win32com.client
# import keyboard

import Window
import Listener

# from time import ctime

######################################################
# Module Installation guide (Need python version from 3.4 - 3.6)
# ---------------------------------------------------
# pip install gTTS
# pip install pyttsx3
# pip install SpeechRecognition
# pip install playsound
# http://www.nirsoft.net/utils/nircmd.html - Download nirCmd to execute commands
# pip install chatterbot
# pip install pillow
# pip install pywin32
# pip install pyaudio
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
		# root.state("zoomed")

		labelText1 = tk.StringVar()
		labelText1.set("")

		labelText2 = tk.StringVar()
		self.label1 = tk.Label(root, textvariable=labelText1, fg='white', bg='#1c1b1b', pady=10, font=("Courier", 20), wraplength=800)
		self.label2 = tk.Label(root, textvariable=labelText2, fg='white', bg='#1c1b1b', pady=10, font=("Courier", 20), wraplength=800)
		self.label1.pack()
		self.label2.pack()

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
			self.speak("HeisenBug.")

		if "you are stupid" in data:
			self.speak("Sorry, if I made some mistake. I won't disappoint you next time.")

		if "who are you" == data:
			self.speak("My name is Walter, a Personal Assistant designed by HeisenBug. I am here to make things easy for you.")

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
			self.searchFolder()

		# if "shutdown the PC" in data:
		#     #Codes to shutdown
		#     self.speak("Shutting down.")
		#     # os.system("poweroff")
		#     os.system('shutdown -s')

		# if "restart the PC" in data:
		#     #Codes to restart
		#     self.speak("Restarting.")
		#     os.system("restart")

		if "lock the PC" in data:
			#Codes to lock the pc
			self.speak("Locking the PC.")
			# os.popen('gnome-screensaver-command --lock')
			os.system("rundll32.exe user32.dll,LockWorkStation")

		if "good bye" in data:
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

		if data.lower().startswith("ping"):
			startIndex = len("ping ")
			sbcName = data[startIndex:]
			self.speak("Pinging " + sbcName)
			self.ping_sbc(sbcName)

		if data.lower().startswith("search jira"):
			self.searchJira()

		if data.lower().startswith("search wiki"):
			self.searchWiki()

		if data.lower().startswith("query jira"):
			self.queryJira()

		if data.lower().startswith("what do i have today"):
			meetings = self.getCalendarEntries()
			numMeetings = len(meetings['Subject'])
			if numMeetings == 0:
				self.speak("You don't have any meetings today.")
			else:
				meetingHour = meetings['StartHour'][0]
				meetingMin = meetings['StartMinute'][0]

				self.speak("You have " + str(numMeetings) + " meeting today. Stating from " + str(meetingHour) + " " + str(meetingMin))

	def main(self):
		welcomeText = "Hello! How can I help you?"

		time.sleep(2)
		self.speak(welcomeText)

		ev = self.getCalendarEntries()
		print(ev)

		while True:
			try:
				data = ""
				data = self.listener.listen()

				if data == -1 or data == -2:
					# self.speak("Sorry, couldn't understand your voice.")
					continue

				labelText = tk.StringVar()
				labelText.set(data)
				self.label1.config(textvariable=labelText)

				self.process(data)
			except KeyboardInterrupt as e:
				print("Exiting...")
				os._exit(0)

	def speak(self, message):
		labelText = tk.StringVar()
		labelText.set(message)
		self.label2.config(textvariable=labelText)

		engine = pyttsx3.init()
		engine.say(message)
		engine.setProperty('volume',0.9)
		engine.runAndWait()

	def ping_sbc(self, sbcName):
		ipsFile = open("config/config.txt", "r")

		sbcIp = ""
		username = ""
		password = ""
		hostIp = ""
		for fileLine in ipsFile:
			if fileLine.startswith("#"):
				continue

			lineLis = fileLine.split(":")
			if lineLis[0] == sbcName :
				sbcIp = lineLis[1].strip()

			if lineLis[0] == "username" :
				username = lineLis[1].strip()

			if lineLis[0] == "password" :
				password = lineLis[1].strip()

			if lineLis[0] == "host_ip" :
				hostIp = lineLis[1].strip()

		ipsFile.close()

		if sbcIp == "" :
			self.speak("SBC IP is not configured.")
			return

		if username == "":
			self.speak("Username is not configured")
			return

		if password == "":
			self.speak("Password is not configured")
			return

		if hostIp == "":
			self.speak("Host IP is not configured")
			return

		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			client.connect(hostIp, 22, username, password)
		except paramiko.AuthenticationException as e:
			self.speak("Authentication Exception Occured")

		command = "ping -w 5 {sbcIp}".format(sbcIp=sbcIp)
		(stdin, stdout, stderr) = client.exec_command(command)
		pingFlag = 0
		for line in stdout.readlines():
		        if re.search( r'.*100% packet loss.*', line, re.M|re.I):
		        	resposes = ["not pinging", "not available", "is down"]
		        	self.speak(sbcName + " is " + resposes[randint(0, len(resposes)-1)])
		        	pingFlag = 1
		        	break

		if pingFlag == 0:
			self.speak(sbcName + " is pinging perfectly")
		client.close()

	def searchJira(self):
		self.speak("Okay, tell me the JIRA ID.")
		data = self.listener.listen()

		dataLis = data.split(" ")
		projectName = dataLis[0].upper()
		jiraId = "".join(dataLis[1:])
		# jiraId = data.replace(" ", "-")

		query = "https://jira.rbbn.com/browse/%s-%s" %(projectName, jiraId)
		print (query)
		self.speak("There you go.")
		webbrowser.open_new_tab(query)

	def searchWiki(self):
		self.speak("Tell me what should I search?")
		data = self.listener.listen()

		query = "https://wiki.sonusnet.com/dosearchsite.action?queryString=%s" %(data)
		print (query)
		self.speak("There you go.")
		webbrowser.open_new_tab(query)

	def queryJira(self):
		self.speak("Sure, tell me what should I search?")
		data = self.listener.listen()
		# filteredData = data.replace(" ", "%20")
		query = "https://jira.rbbn.com/issues/?jql=text%20~%20\"" + data +"\"%20ORDER%20BY%20updated%20DESC"
		self.speak("There you go.")
		webbrowser.open_new_tab(query)

	def getCalendarEntries(self, days=1):
		"""
		Returns calender entries for days default is 1
		"""
		Outlook = win32com.client.Dispatch("Outlook.Application")
		ns = Outlook.GetNamespace("MAPI")
		appointments = ns.GetDefaultFolder(9).Items
		appointments.Sort("[Start]")
		appointments.IncludeRecurrences = "True"
		today = datetime.datetime.today()
		begin = today.date().strftime("%d/%m/%Y")
		tomorrow= datetime.timedelta(days=days)+today
		end = tomorrow.date().strftime("%d/%m/%Y")
		appointments = appointments.Restrict("[Start] >= '" +begin+ "' AND [END] <= '" +end+ "'")
		events={'StartHour':[], 'StartMinute':[], 'Subject':[],'Duration':[]}
		for a in appointments:
			# adate=datetime.datetime.fromtimestamp(int(a.Start))
			meetingStart = str(a.Start)
			(date, time) =meetingStart.split(" ")
			(hour, minute, junk1, junk2) = time.split(":")

			events['StartHour'].append(hour)
			events['StartMinute'].append(minute)
			events['Subject'].append(a.Subject)
			events['Duration'].append(a.Duration)
		return events

	# Search for a folder
	def searchFolder(self):
		self.speak("Okay, tell me the name of the folder.")

		# Home directories
		# spaths = [r"/home/soumya/", r"/media/soumya/Docs/", r"/media/soumya/Entertainment/"]
		spaths= [r"D:\\"]

		folderName = self.listener.listen()
		folderName = folderName.lower()
		self.speak("Searching, Please wait.")
		print("Searching...")

		flag = 0
		while(len(spaths) > 0):
			currentPath = spaths[0]
			print("Currently searching: "+currentPath)
			root, dirs, _ = next(os.walk(currentPath))


			for dir in dirs:
				if folderName.lower() == str(dir).lower():
					self.speak("There you go.")
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
			self.speak("Sorry, specified directory not found.")


if __name__ == '__main__':
	# root = tk.Tk()
	# window = Window.Window(root)
	# # window.setVars("siri.gif")
	# window.pack()
	# window.load("siri.gif")
	# window.mainloop()

	assitant = Assistant("siri.gif")
	assitant.main()
