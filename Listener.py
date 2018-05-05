# import Window
import threading
import speech_recognition as sr

class Listener(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.start()

	def listen(self):
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

	            return -1
	        except sr.RequestError as e:
	            print("Could not request results from Google Speech Recognition service; {0}".format(e))

	            return -2

	    return data