import logging
from os import path
from threading import Thread
from playsound import playsound


logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')

def notify_sound():
    sound = path.join(path.dirname(__file__),".." ,"ui", "notification.wav")
    logging.debug(sound)
    Thread(target=playsound, args=(sound,), daemon=True).start()
